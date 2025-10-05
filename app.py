import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2 
import matplotlib.pyplot as plt
import time
import json

# -----------------
# 1. Configuración de la Página
# -----------------

st.set_page_config(
    page_title="AI Cacao | Detección de Moniliasis",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/GulagWinner',
        'Report a bug': "https://github.com/GulagWinner/issues",
        'About': "# AI Cacao - Detector de Moniliasis\n Esta aplicación utiliza IA para detectar moniliasis en mazorcas de cacao."
    }
)

# Estilo personalizado
st.markdown("""
    <style>
        /* Estilos generales */
        .stApp {
            background: #f0f2f6;
        }
        .main > div {
            padding: 2rem;
            border-radius: 10px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Estilos de la barra lateral */
        .stSidebar > div {
            padding: 2rem;
            background: #2c3e50;
        }
        .stSidebar [data-testid="stMarkdown"] {
            color: white !important;
        }
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label {
            color: white !important;
        }
        .stSidebar [data-testid="stFileUploader"] {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 1rem;
            border-radius: 10px;
        }
        
        /* Estilos de texto y contenido */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50 !important;
            font-family: 'Helvetica Neue', sans-serif !important;
        }
        p, li, span {
            color: #34495e !important;
        }
        a {
            color: #3498db !important;
        }
        
        /* Estilos de componentes */
        .stButton>button {
            background-color: #27ae60 !important;
            color: white !important;
            font-weight: bold !important;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            border: none !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton>button:hover {
            background-color: #219a52 !important;
            border: none !important;
        }
        
        /* Estilos de métricas y progreso */
        [data-testid="stMetricValue"] {
            color: #2c3e50 !important;
            font-size: 2rem !important;
            font-weight: bold !important;
        }
        [data-testid="stMetricDelta"] svg {
            display: none;
        }
        [data-testid="stMetricLabel"] {
            color: #666 !important;
        }
        .stProgress > div > div > div {
            background-color: #27ae60;
        }
        
        /* Estilos de cards y contenedores */
        [data-testid="stExpander"] {
            background-color: white !important;
            border-radius: 10px !important;
            border: 1px solid #e0e0e0 !important;
            overflow: hidden;
        }
        
        /* Estilos de alerts e info */
        .stAlert {
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
            border: none !important;
            border-radius: 10px;
        }
        
        /* Estilos de tabs */
        .stTabs [data-baseweb="tab"] {
            font-size: 1rem !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            background-color: transparent !important;
            border-radius: 4px;
            margin-right: 1rem;
        }
        .stTabs [aria-selected="true"] {
            color: #27ae60 !important;
            border-bottom: 2px solid #27ae60 !important;
        }
        
        /* Ajustes de contraste para textos */
        div.row-widget.stRadio > div {
            color: #2c3e50 !important;
        }
        div.row-widget.stSelectbox > div > div {
            color: #2c3e50 !important;
        }
        .element-container .stMarkdown p {
            color: #2c3e50 !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------
# 2. Configuración y Carga de Nombres de Clases
# -----------------

UMBRAL_CONFIANZA_NO_CACO = 70.0
MODEL_PATH = "cacao_resnet101_classifier3.keras"

try:
    with open('class_names.json', 'r') as f:
        class_names = json.load(f)
except FileNotFoundError:
    st.error("Error: El archivo 'class_names.json' no se encontró. Asegúrate de que esté en la misma carpeta que app.py.")
    st.stop()

# -----------------
# 3. Funciones de Preprocesamiento y Saliency Map
# -----------------

@st.cache_resource
def load_model(path):
    try:
        model = tf.keras.models.load_model(path)
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo. Verifique la ruta y el formato. Error: {e}")
        st.stop()

def preprocess_image_for_prediction_resnet(image_array, target_size=(224, 224)):
    img_resized = Image.fromarray(image_array.astype(np.uint8)).resize(target_size)
    img_array_resized = np.asarray(img_resized, dtype=np.float32)
    img_preprocessed = tf.keras.applications.resnet_v2.preprocess_input(np.expand_dims(img_array_resized, axis=0))
    return img_preprocessed

def extract_numerical_features_for_prediction(image_stream):
    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
    img_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img_bgr is None:
        return np.array([0.0, 0.0, 0.0], dtype=np.float32)

    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, black_mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
    percentage_black = (np.sum(black_mask > 0) / np.prod(img_bgr.shape[:2])) * 100

    num_labels, _, stats, _ = cv2.connectedComponentsWithStats(black_mask, 8, cv2.CV_32S)
    large_black_spots_count = sum(1 for i in range(1, num_labels) if stats[i, cv2.CC_STAT_AREA] > 100)

    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    mean_green_value = np.mean(hsv[:, :, 2][green_mask > 0]) if np.sum(green_mask > 0) > 0 else 0

    max_percentage_black = 100.0
    max_spots = 20
    max_green_value = 255.0

    scaled_percentage_black = percentage_black / max_percentage_black
    scaled_large_black_spots_count = min(large_black_spots_count / max_spots, 1.0)
    scaled_mean_green_value = mean_green_value / max_green_value

    return np.array([scaled_percentage_black, scaled_large_black_spots_count, scaled_mean_green_value], dtype=np.float32)

def get_prediction_info(model, image_path, preprocess_img_fn, extract_features_fn, confidence_threshold):
    original_img_pil = Image.open(image_path).convert('RGB')
    original_img_array = np.asarray(original_img_pil)

    preprocessed_img_for_resnet = preprocess_img_fn(original_img_array)
    img_tensor = tf.Variable(preprocessed_img_for_resnet, dtype=tf.float32)

    image_path.seek(0)
    numerical_features = extract_features_fn(image_path)
    numerical_features_batch = np.expand_dims(numerical_features, axis=0)
    numerical_features_tensor = tf.convert_to_tensor(numerical_features_batch, dtype=tf.float32)

    with tf.GradientTape() as tape:
        tape.watch(img_tensor)
        predictions = model([img_tensor, numerical_features_tensor])
        predicted_class_idx = tf.argmax(predictions[0])
        predicted_class_score = predictions[0, predicted_class_idx]
    
    gradients = tape.gradient(predicted_class_score, img_tensor)
    gradients = gradients[0].numpy()
    saliency_map = np.sum(np.abs(gradients), axis=-1)
    saliency_map = np.maximum(saliency_map, 0)
    if np.max(saliency_map) > 0:
        saliency_map /= np.max(saliency_map)

    saliency_map_colored = cv2.applyColorMap(np.uint8(255 * saliency_map), cv2.COLORMAP_JET)
    saliency_map_colored = cv2.cvtColor(saliency_map_colored, cv2.COLOR_BGR2RGB)
    saliency_map_resized = cv2.resize(saliency_map_colored, (original_img_array.shape[1], original_img_array.shape[0]))
    overlayed_image = cv2.addWeighted(original_img_array.astype(np.uint8), 0.6, saliency_map_resized, 0.4, 0)
    
    confidence = predictions[0, predicted_class_idx].numpy() * 100
    predicted_class_name_raw = class_names[predicted_class_idx.numpy()]
    
    if confidence < UMBRAL_CONFIANZA_NO_CACO:
        final_prediction_text = f"NO ES UNA MAZORCA DE CACAO. (Confianza: {confidence:.2f}%)"
        display_title_text = "NO MAZORCA"
    else:
        final_prediction_text = f"Es una mazorca de cacao: {predicted_class_name_raw} (Confianza: {confidence:.2f}%)"
        display_title_text = f"{predicted_class_name_raw}"
    
    return overlayed_image, final_prediction_text, display_title_text

# -----------------
# 4. Diseño de la Interfaz y Lógica Principal
# -----------------

# Inicializa el estado de la sesión
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'history' not in st.session_state:
    st.session_state.history = []

def add_to_history(image, prediction, confidence):
    """Agrega una imagen analizada al historial"""
    history_item = {
        'image': image,
        'prediction': prediction,
        'confidence': confidence,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.history.insert(0, history_item)  # Agregar al inicio
    if len(st.session_state.history) > 10:  # Mantener solo las últimas 10 imágenes
        st.session_state.history.pop()

# Barra lateral para la carga de archivos
with st.sidebar:
    st.header("Sube tu imagen")
    temp_uploaded_file = st.file_uploader("Elige una imagen de una mazorca...", type=["jpg", "png", "jpeg"])
    
    if temp_uploaded_file:
        st.session_state.uploaded_file = temp_uploaded_file
        if st.button("Analizar Imagen"):
            st.session_state.analyzed = True
    
    if temp_uploaded_file is None and st.session_state.uploaded_file is not None:
        st.session_state.analyzed = False
        st.session_state.uploaded_file = None
        st.rerun()

# Título principal
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>🌿 AI Cacao | Detector de Moniliasis</h1>
        <p style='font-size: 1.2em; color: #666;'>Sistema inteligente de detección de enfermedades en mazorcas de cacao</p>
    </div>
""", unsafe_allow_html=True)

# Tabs de navegación
tab1, tab2 = st.tabs(["📸 Análisis", "📊 Historial"])

with tab1:
    if not st.session_state.analyzed:
        st.info("🔍 Sube una imagen desde la barra lateral para comenzar el análisis.")
        
        # Información del proyecto
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                ### 🎯 Objetivo
                Detectar de manera precisa la presencia de moniliasis en mazorcas de cacao utilizando IA.
            """)
        with col2:
            st.markdown("""
                ### 📋 Instrucciones
                1. Sube una imagen clara
                2. Presiona "Analizar Imagen"
                3. Revisa los resultados
            """)
        with col3:
            st.markdown("""
                ### 💡 Beneficios
                - Detección temprana
                - Análisis preciso
                - Resultados instantáneos
            """)

    elif st.session_state.analyzed and st.session_state.uploaded_file:
        st.markdown("""
            <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
                <h2>🔍 Resultados del Análisis</h2>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <div style='padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h3 style='text-align: center; color: #2c3e50;'>📸 Imagen Analizada</h3>
                </div>
            """, unsafe_allow_html=True)
            image = Image.open(st.session_state.uploaded_file)
            st.image(image, use_column_width=True)

        with col2:
            with st.spinner("🔄 Procesando imagen..."):
                time.sleep(1)
                try:
                    overlayed_img, final_pred_text, display_title = get_prediction_info(
                        load_model(MODEL_PATH),
                        st.session_state.uploaded_file,
                        preprocess_image_for_prediction_resnet,
                        extract_numerical_features_for_prediction,
                        UMBRAL_CONFIANZA_NO_CACO
                    )
                    
                    # Extraer el porcentaje de confianza
                    confidence_str = final_pred_text.split("Confianza: ")[1].rstrip("%)").strip()
                    confidence = float(confidence_str)
                    
                    # Agregar al historial
                    add_to_history(st.session_state.uploaded_file, display_title, confidence)
                    
                    # Mostrar resultados
                    st.markdown("""
                        <div style='padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h3 style='text-align: center; color: #2c3e50;'>📊 Resultados</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Métrica de confianza
                    st.metric(
                        label="Nivel de Confianza",
                        value=f"{confidence:.1f}%",
                        delta=f"{confidence-50:.1f}%" if confidence > 50 else f"-{50-confidence:.1f}%"
                    )
                    
                    # Resultado principal
                    st.markdown(f"""
                        <div style='text-align: center; padding: 1rem; background-color: {'#e74c3c' if 'NO ES' in final_pred_text else '#27ae60'}; 
                                color: white; border-radius: 10px; margin: 1rem 0;'>
                            <h4 style='margin: 0;'>{final_pred_text}</h4>
                        </div>
                    """, unsafe_allow_html=True)

                    # Mapa de calor
                    st.markdown("""
                        <div style='padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h4 style='text-align: center; color: #2c3e50;'>🎯 Áreas de Interés</h4>
                        </div>
                    """, unsafe_allow_html=True)
                    fig_sal, ax_sal = plt.subplots(figsize=(4, 4))
                    ax_sal.imshow(overlayed_img)
                    ax_sal.set_title(f'Análisis: {display_title}', color='#333')
                    ax_sal.axis('off')
                    st.pyplot(fig_sal)

                except Exception as e:
                    st.error(f"❌ Error en el análisis: {e}")

with tab2:
    st.markdown("""
        <div style='text-align: center; padding: 1rem; margin-bottom: 2rem;'>
            <h2>📚 Historial de Análisis</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        for i in range(0, len(st.session_state.history), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(st.session_state.history):
                    item = st.session_state.history[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div style='padding: 1rem; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                <p style='color: #666; font-size: 0.8em;'>{item['timestamp']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        st.image(item['image'], caption=f"Predicción: {item['prediction']}", use_column_width=True)
                        st.progress(item['confidence']/100)
                        st.markdown(f"Confianza: {item['confidence']:.1f}%")
    else:
        st.info("📝 El historial está vacío. Analiza algunas imágenes para empezar a registrar resultados.")