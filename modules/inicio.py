import streamlit as st

def render():
    st.markdown('<div class="page-card">', unsafe_allow_html=True)
    st.title("Suite Multimedia — Herramientas de IA y Procesamiento")
    st.markdown("**Kit de herramientas** para conversión de audio, OCR, NLP, detección de objetos y más.")

    st.markdown("### Qué contiene este sitio")
    st.markdown(
        """
- **Texto → Audio (gTTS)**: escribir texto y generar audio en MP3.
- **Voz → Texto (Vosk)**: subir o grabar audio WAV y transcribir sin depender de ffmpeg.
        """
    )

    st.markdown("### Navegación")
    st.markdown("Usa el menú lateral para elegir la herramienta.")

    st.markdown("</div>", unsafe_allow_html=True)
