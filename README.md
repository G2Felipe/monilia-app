
# 🍫 Monilia Detector

Solución web integral para la detección temprana de moniliasis en mazorcas de cacao, combinando IA y una experiencia de usuario moderna. Pensado para agricultores, técnicos y laboratorios agrícolas.

---

## 🚀 Funcionalidades Clave

- 📷 Subida de imágenes de mazorcas y predicción instantánea de moniliasis.
- 🧠 Backend robusto con FastAPI y modelo ResNet101 optimizado.
- 💻 Frontend intuitivo y responsive con Next.js y Tailwind CSS.
- 📑 Documentación automática de la API y endpoints claros.
- 🕒 Historial de predicciones en la sesión del usuario.
- ☁️ Despliegue sencillo en Vercel (frontend) y Render (backend).

---

## 🏗️ Tecnologías Principales

<p>
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.110.0-green?logo=fastapi"/>
  <img src="https://img.shields.io/badge/TensorFlow-2.20-orange?logo=tensorflow"/>
  <img src="https://img.shields.io/badge/Next.js-15-black?logo=next.js"/>
  <img src="https://img.shields.io/badge/TailwindCSS-3.x-06B6D4?logo=tailwindcss"/>
  <img src="https://img.shields.io/badge/Deployed-Vercel%20%7C%20Render-000?logo=vercel"/>
</p>

---

## 📁 Estructura General

```
monilia-app/
├── backend/      # Lógica de API y modelo IA
├── frontend/     # Interfaz Next.js + Tailwind
├── docs/         # Documentación extendida
├── cacao_resnet101_classifier3.keras
├── class_names.json
└── README.md
```

---

## ⚡ Instalación Rápida

**Requisitos:** 🐍 Python 3.13+, 🟩 Node.js 18+, 🟦 npm

1️⃣ Clona el repositorio:
```bash
git clone https://github.com/G2Felipe/monilia-app.git
cd monilia-app
```
2️⃣ Instala y ejecuta el backend:
```bash
cd backend
python -m venv env
env\Scripts\activate
pip install -r requirements.txt
python main.py
```
3️⃣ Instala y ejecuta el frontend:
```bash
cd ../frontend
npm install
npm run dev
```

---

## 🔗 Endpoints Principales

- **POST `/predict`**: Recibe una imagen y retorna la predicción de moniliasis.
- **GET `/health`**: Devuelve el estado del backend y del modelo IA.

---

## 🛠️ Stack y Decisiones Técnicas

- 🐍 **Python 3.13**: Robustez y compatibilidad con IA.
- ⚡ **FastAPI**: APIs rápidas, seguras y con Swagger.
- 🔶 **TensorFlow 2.20**: Framework de IA para ResNet101.
- 🖼️ **Pillow, NumPy, OpenCV**: Procesamiento eficiente de imágenes.
- ⚛️ **Next.js 15**: SSR y experiencia moderna en React.
- 🎨 **Tailwind CSS**: Diseño responsive y utilitario.
- ▲ **Vercel**: Hosting optimizado para Next.js.
- 🟪 **Render**: Ideal para backend Python y archivos grandes.

**¿Por qué esta arquitectura?**
Permite separar la lógica de negocio (backend) de la experiencia de usuario (frontend), facilitando mantenimiento, escalabilidad y despliegue independiente.

---

## 🧩 Troubleshooting

- ❗ Si el modelo no carga, asegúrate de que los archivos `.keras` y `.json` estén en la raíz.
- 🔄 Si hay errores de dependencias, reinstala con los requirements.
- 🌐 Si el frontend no conecta, revisa la URL del backend en el código fuente.
- 🩺 Usa el endpoint `/health` para verificar el estado del backend.

---

## 📝 Mejoras Futuras

- 🗃️ Persistencia de historial de predicciones (base de datos)
- 🔐 Autenticación y roles de usuario
- 📊 Exportación de reportes y estadísticas
- 📈 Dashboard de monitoreo
- 🚀 Optimización del modelo (ONNX, TensorRT)
- 📱 PWA y soporte offline
- 🧪 Tests automáticos y CI/CD

---

## 🤝 Cómo Contribuir

1. Haz fork del repositorio
2. Crea una rama para tu mejora o fix
3. Haz commit y push
4. Abre un Pull Request

---

## 📄 Licencia

MIT License. Consulta el archivo LICENSE para más detalles.

---

## 🙌 Créditos y Reconocimientos

Desarrollado con FastAPI, Next.js y TensorFlow.
Agradecimientos a las comunidades de [TensorFlow](https://www.tensorflow.org/), [FastAPI](https://fastapi.tiangolo.com/), [Next.js](https://nextjs.org/), [Render](https://render.com/) y [Vercel](https://vercel.com/).

Desarrollado Por:
Andrés Felipe Fonseca Gaona 
Daniel Felipe Alonso Vaca
Michell Stiven Barreto Cruz
