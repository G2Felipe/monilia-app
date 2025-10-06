from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2
import io
import json
from typing import Optional
import os
from datetime import datetime

app = FastAPI(
    title="AI Cacao API",
    description="API para la detección de moniliasis en mazorcas de cacao",
    version="1.0.0"
)

# La configuración de CORS se realiza después de crear todas las rutas

# Cargar el modelo y las clases
# Detectar entorno y configurar rutas
if os.path.exists('/opt/render/project/src/cacao_resnet101_classifier3.keras'):
    # Entorno Render
    MODEL_PATH = '/opt/render/project/src/cacao_resnet101_classifier3.keras'
    CLASS_NAMES_PATH = '/opt/render/project/src/class_names.json'
elif os.path.exists(os.path.join(os.path.dirname(os.getcwd()), "cacao_resnet101_classifier3.keras")):
    # Entorno local desde backend/
    MODEL_PATH = os.path.join(os.path.dirname(os.getcwd()), "cacao_resnet101_classifier3.keras")
    CLASS_NAMES_PATH = os.path.join(os.path.dirname(os.getcwd()), "class_names.json")
else:
    # Fallback: buscar en el directorio actual
    MODEL_PATH = "cacao_resnet101_classifier3.keras"
    CLASS_NAMES_PATH = "class_names.json"

UMBRAL_CONFIANZA_NO_CACAO = 70.0

print(f"MODEL_PATH: {MODEL_PATH}")
print(f"CLASS_NAMES_PATH: {CLASS_NAMES_PATH}")
print(f"Current working directory: {os.getcwd()}")
print(f"Parent directory: {os.path.dirname(os.getcwd())}")

# Listar archivos en el directorio actual y padre
try:
    print(f"Files in current directory: {os.listdir('.')}")
    print(f"Files in parent directory: {os.listdir('..')}")
except Exception as e:
    print(f"Error listing directories: {e}")

# Variables globales para el modelo y las clases
model = None
class_names = None
model_loaded = False

def check_file_exists(file_path):
    exists = os.path.exists(file_path)
    print(f"Verificando archivo {file_path}: {'existe' if exists else 'no existe'}")
    if not exists:
        print(f"Directorio actual: {os.getcwd()}")
        print(f"Contenido del directorio: {os.listdir()}")
    return exists

def load_model_and_classes():
    """Carga el modelo y clases de manera diferida (lazy loading)"""
    global model, class_names, model_loaded
    
    if model_loaded:
        return True  # Ya está cargado
    
    print("Cargando modelo y clases por primera vez...")
    
    # Verificar archivos
    if not check_file_exists(CLASS_NAMES_PATH) or not check_file_exists(MODEL_PATH):
        print("Error: Archivos necesarios no encontrados")
        return False
    
    # Cargar nombres de clases
    try:
        print("Cargando archivo de clases...")
        with open(CLASS_NAMES_PATH, 'r') as f:
            class_names = json.load(f)
            print("Archivo de clases cargado exitosamente")
    except Exception as e:
        print(f"Error al cargar archivo de clases: {str(e)}")
        return False

    # Cargar modelo
    try:
        print("Cargando modelo de TensorFlow...")
        model = tf.keras.models.load_model(MODEL_PATH)
        model_loaded = True
        print("Modelo cargado exitosamente")
        return True
    except Exception as e:
        print(f"Error al cargar el modelo: {str(e)}")
        return False

# NO cargar el modelo al inicio para ahorrar memoria
print("API iniciada. El modelo se cargará en la primera predicción.")

def preprocess_image(image_bytes):
    """Preprocesa la imagen para el modelo"""
    try:
        # Convertir bytes a imagen
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        image_array = np.asarray(image)
        
        # Redimensionar
        img_resized = cv2.resize(image_array, (224, 224))
        img_array_resized = np.asarray(img_resized, dtype=np.float32)
        
        # Preprocesar para ResNet
        img_preprocessed = tf.keras.applications.resnet_v2.preprocess_input(
            np.expand_dims(img_array_resized, axis=0)
        )
        
        return img_preprocessed, image_array
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al procesar la imagen: {str(e)}")

def extract_features(image_array):
    """Extrae características numéricas de la imagen"""
    try:
        # Convertir a BGR para OpenCV
        img_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Características de manchas negras
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        _, black_mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        percentage_black = (np.sum(black_mask > 0) / np.prod(img_bgr.shape[:2])) * 100

        # Conteo de manchas grandes
        num_labels, _, stats, _ = cv2.connectedComponentsWithStats(black_mask, 8, cv2.CV_32S)
        large_black_spots = sum(1 for i in range(1, num_labels) if stats[i, cv2.CC_STAT_AREA] > 100)

        # Características de color verde
        hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
        mean_green = np.mean(hsv[:, :, 2][green_mask > 0]) if np.sum(green_mask > 0) > 0 else 0

        # Normalizar características
        scaled_black = percentage_black / 100.0
        scaled_spots = min(large_black_spots / 20.0, 1.0)
        scaled_green = mean_green / 255.0

        return np.array([[scaled_black, scaled_spots, scaled_green]], dtype=np.float32)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al extraer características: {str(e)}")

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    """Endpoint para predicción de imágenes"""
    # Cargar modelo si no está cargado aún
    if not model_loaded:
        if not load_model_and_classes():
            raise HTTPException(
                status_code=503, 
                detail="Error al cargar el modelo. Intente nuevamente."
            )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail="El archivo debe ser una imagen"
        )
    
    try:
        # Leer imagen
        contents = await file.read()
        img_preprocessed, original_image = preprocess_image(contents)
        
        # Extraer características
        numerical_features = extract_features(original_image)
        
        # Realizar predicción
        predictions = model([
            tf.convert_to_tensor(img_preprocessed), 
            tf.convert_to_tensor(numerical_features)
        ])
        
        # Procesar resultados
        predicted_class_idx = tf.argmax(predictions[0]).numpy()
        confidence = float(predictions[0][predicted_class_idx] * 100)
        predicted_class = class_names[predicted_class_idx]
        
        # Determinar resultado
        is_cacao = confidence >= UMBRAL_CONFIANZA_NO_CACAO
        
        return JSONResponse({
            "success": True,
            "prediction": {
                "is_cacao": is_cacao,
                "class_name": predicted_class,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        print(f"Error en la predicción: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    return {
        "status": "ready",
        "model_loaded": model_loaded,
        "classes_loaded": class_names is not None,
        "model_path": MODEL_PATH,
        "class_names_path": CLASS_NAMES_PATH,
        "memory_optimized": True
    }

from fastapi.middleware.cors import CORSMiddleware

# Configurar CORS después de crear la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Desarrollo local
        "https://monilia-8sco96gob-felipes-projects-4bcfded5.vercel.app",  # Tu dominio actual de Vercel
        "https://*.vercel.app",  # Permitir cualquier subdominio de Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")