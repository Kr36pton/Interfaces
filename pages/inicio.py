import streamlit as st

def render():
    st.markdown('<div class="page-card">', unsafe_allow_html=True)
    st.title("Suite Multimedia — Herramientas de IA y Procesamiento")
    st.markdown("**Kit de herramientas** para conversión de audio, OCR, NLP, detección de objetos y más.")
    st.image(
        "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=1400&q=80",
        caption="Interfaz unificada — herramientas modulares",
        use_column_width=True,
    )

    st.markdown("### Qué contiene este sitio")
    st.markdown(
        """
- **Texto → Audio (gTTS)**: caja de texto para convertir a audio reproducible y descargable.
- **Voz → Texto (Whisper)**: subir/grabar audio, transcripción automática y selección de idioma.
- **OCR (Imagen → Texto)**: cargar imágenes/PDFs para extraer texto digital.
- **OCR → Traducción → Audio**: extrae texto, traduce al idioma seleccionado y genera audio en ese idioma.
- **NLP (TextBlob / NLTK)**: análisis de sentimiento y subjetividad; extracción de palabras clave; TF-IDF; pregunta-respuesta sobre el texto con validación de ausencia de respuesta.
- **Detección de Objetos (YOLO)**: detección en imágenes y devolución de imagen con bounding boxes.
- **Reconocimiento de Gestos (Teachable Machine)**: detector en tiempo real (webcam) y desde foto usando modelo exportado.
- **Chatbot sobre PDF (LLM)**: subir PDF de materia específica y realizar preguntas contextuales.
- **Descripción de Imágenes y QA**: generar descripción detallada de una imagen y permitir preguntas sobre la misma.
        """
    )

    st.markdown("### Índice rápido")
    st.markdown(
        """
1. Navegar por el menú lateral a la página deseada.
2. Cada herramienta cuenta con su propia página en `/pages/` (modular).
3. Trabajaremos página por página: la primera entrega es esta página de inicio.
        """
    )

    st.markdown("**Referencia del documento de especificaciones.** :contentReference[oaicite:1]{index=1}")
    st.markdown("</div>", unsafe_allow_html=True)
