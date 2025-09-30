import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import io
from gtts import gTTS
import tempfile
import uuid
from googletrans import Translator

def render():
    st.title("OCR → Traducción → Audio")
    st.markdown("Extrae texto de una imagen, tradúcelo a otro idioma y genera audio descargable.")

    # Cargar imagen
    uploaded_file = st.file_uploader(
        "Sube una imagen (JPG, PNG, TIFF, BMP)",
        type=["jpg", "jpeg", "png", "tiff", "bmp"]
    )

    # Selección de idioma destino
    target_lang = st.selectbox(
        "Selecciona el idioma de traducción",
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

    if uploaded_file:
        image = Image.open(io.BytesIO(uploaded_file.read()))
        st.image(image, caption="Imagen cargada", use_container_width=True)

        if st.button("Procesar"):
            with st.spinner("Extrayendo texto..."):
                reader = easyocr.Reader(['es','en'])
                result = reader.readtext(np.array(image), detail=0)
                extracted_text = "\n".join(result).strip()

            if not extracted_text:
                st.warning("No se detectó texto en la imagen.")
                return

            st.markdown("### Texto detectado")
            st.text_area("Resultado OCR", extracted_text, height=200)

            with st.spinner("Traduciendo texto..."):
                translator = Translator()
                translation = translator.translate(extracted_text, dest=target_lang).text

            st.markdown("### Traducción")
            st.text_area("Texto traducido", translation, height=200)

            with st.spinner("Generando audio..."):
                try:
                    tts = gTTS(text=translation, lang=target_lang)
                    tmp_fp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                    tts.save(tmp_fp.name)
                except Exception as e:
                    st.error(f"Error al generar audio: {e}")
                    return

            with open(tmp_fp.name, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")

            filename = f"ocr_traduccion_{uuid.uuid4().hex[:8]}.mp3"
            st.download_button(
                "Descargar audio",
                data=audio_bytes,
                file_name=filename,
                mime="audio/mpeg"
            )
