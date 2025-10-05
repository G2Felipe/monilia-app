# Monilia App - Backend

Backend API para la detección de moniliasis en mazorcas de cacao usando FastAPI y TensorFlow.

## Despliegue en Render

Este proyecto está configurado para desplegarse fácilmente en Render usando **Python 3.13**.

### Archivos de configuración:
- `runtime.txt`: Especifica Python 3.13.0 (última versión compatible)
- `Procfile`: Comando para iniciar la aplicación
- `backend/requirements.txt`: Librerías optimizadas para Python 3.13

### Librerías actualizadas para Python 3.13:
- **FastAPI 0.115.6**: Versión más reciente
- **Pillow 11.0.0**: Compatible con Python 3.13
- **TensorFlow 2.18.0**: Última versión estable
- **NumPy 2.1.3**: Compatible con Python 3.13
- **OpenCV 4.10.0.84**: Versión más reciente

### Configuración en Render:
1. Conecta tu repositorio de GitHub
2. Build Command: `pip install -r backend/requirements.txt`
3. Start Command: `uvicorn backend.main:app --host=0.0.0.0 --port=10000`
4. Environment: Python 3 (Render detectará automáticamente Python 3.13)

### Endpoints:
- `GET /health`: Verificar estado de la API
- `POST /predict`: Realizar predicción de imagen

### Variables de entorno (opcionales):
- `PORT`: Puerto del servidor (por defecto 10000)
- `CORS_ORIGINS`: Orígenes permitidos para CORS

