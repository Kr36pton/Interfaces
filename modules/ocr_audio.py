import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from googletrans import Translator
from gtts import gTTS
import tempfile
import io
import uuid

def render():
    st.title("OCR → Traducción → Audio")
    st.markdown("Extrae texto de imágenes, tradúcelo y genera audio en el idioma deseado.")

    # Cargar imagen
    uploaded_file = st.file_uploader(
        "Sube una imagen (JPG, PNG, JPEG)",
        type=["jpg", "jpeg", "png"]
    )

    # Idioma destino para la traducción y audio
    target_lang = st.selectbox(
        "Selecciona idioma de destino",
        [
            ("es", "Español"),
            ("en", "Inglés"),
            ("fr", "Francés"),
            ("de", "Alemán"),
            ("it", "Italiano"),
            ("pt", "Portugués")
        ],
        format_func=lambda x: x[1]
    )[0]

    if uploaded_file is not None:
        # Mostrar imagen
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_container_width=True)

        if st.button("Procesar imagen"):
            # OCR con EasyOCR
            with st.spinner("Ejecutando OCR..."):
                reader = easyocr.Reader(['es', 'en'])
                result = reader.readtext(np.array(image), detail=0)
                text = "\n".join(result).strip()

            if not text:
                st.warning("No se detectó texto en la imagen.")
                return

            st.markdown("### Texto detectado")
            st.text_area("OCR", text, height=200)

            # Traducción con Googletrans
            with st.spinner("Traduciendo texto..."):
                translator = Translator()
                translation = translator.translate(text, dest=target_lang).text

            st.markdown("### Traducción")
            st.text_area("Traducción", translation, height=200)

            # Conversión a audio con gTTS
            with st.spinner("Generando audio..."):
                try:
                    tts = gTTS(text=translation, lang=target_lang)
                    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tts.save(tmp_file.name)
                except Exception as e:
                    st.error(f"Error al generar audio: {e}")
                    return

            # Reproducir y descargar
            with open(tmp_file.name, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3")

            filename = f"ocr_traduccion_{uuid.uuid4().hex[:8]}.mp3"
            st.download_button(
                "Descargar audio",
                data=audio_bytes,
                file_name=filename,
                mime="audio/mpeg"
            )
