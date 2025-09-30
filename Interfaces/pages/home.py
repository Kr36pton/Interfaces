import streamlit as st




def app():
st.title("Suite de Herramientas Multimodales")


st.markdown("## Introducción")
st.markdown(
"Este sitio reúne utilidades para procesamiento de audio, voz, imágenes y texto.\n\n"
"Use la barra lateral izquierda para navegar entre las herramientas.\n\n"
"Cada herramienta está implementada como una página independiente dentro de `Interfaces/pages/`."
)


st.image(
"https://via.placeholder.com/1000x300.png?text=Herramientas+Multimodales",
use_column_width=True,
)


st.markdown("---")


st.markdown("### Índice de herramientas (rápido)")
st.markdown(
"- **Texto → Audio** — convierte texto en MP3 reproducible y descargable.\n"
"- **Voz → Texto** — transcripción con Whisper y selección de idioma.\n"
"- **OCR (Imagen → Texto)** — extrae texto de imágenes o PDF.\n"
"- **OCR + Traducción + Audio** — OCR, traducir y generar audio en el idioma seleccionado.\n"
"- **NLP (TextBlob / NLTK)** — análisis de sentimiento, extracción de keywords, TF-IDF y preguntas sobre el texto.\n"
"- **Detección de Objetos (YOLO)** — detecta objetos y dibuja cajas delimitadoras.\n"
"- **Identificación de Gestos** — detector en tiempo real (modelo de Teachable Machine) y desde imágenes.\n"
"- **Chatbot con PDF (LLM)** — interactúa con documentos PDF mediante LLM.\n"
"- **Interpretación de Imágenes** — descripción detallada de la imagen y preguntas sobre ella."
)


st.markdown("---")
st.markdown("**Estado actual:** Página de inicio implementada. Avanzaremos página por página según la solicitud.")
