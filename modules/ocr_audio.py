import streamlit as st
from PIL import Image
import numpy as np
import easyocr
from googletrans import Translator
from gtts import gTTS
import tempfile
import uuid

def render():
    st.title("OCR → Traducción → Audio")
    st.markdown("Extrae texto de imágenes, tradúcelo y genera audio en el idioma seleccionado.")

    uploaded_file = st.file_uploader("Sube una imagen (JPG o PNG)", type=["jpg", "jpeg", "png"])

    target_lang = st.selectbox(
        "Idioma destino",
        [("es", "Español"), ("en", "Inglés"), ("fr", "Francés"),
         ("de", "Alemán"), ("it", "Italiano"), ("pt", "Portugués")],
        format_func=lambda x: x[1]
    )[0]

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagen cargada", use_container_width=True)

        if st.button("Procesar"):
            with st.spinner("Ejecutando OCR..."):
                reader = easyocr.Reader(['es', 'en'])
                result = reader.readtext(np.array(image), detail=0)
                extracted_text = "\n".join(result).strip()

            if not extracted_text:
                st.warning("No se detectó texto en la imagen.")
                return

            st.markdown("### Texto detectado")
            st.text_area("Texto OCR", extracted_text, height=200)

            with st.spinner("Traduciendo texto..."):
                translator = Translator()
                translated = translator.translate(extracted_text, dest=target_lang).text

            st.markdown("### Traducción")
            st.text_area("Texto traducido", translated, height=200)

            with st.spinner("Generando audio..."):
                tts = gTTS(text=translated, lang=target_lang)
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
                tts.save(tmp.name)

            with open(tmp.name, "rb") as f:
                audio_bytes = f.read()

            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                "Descargar audio",
                data=audio_bytes,
                file_name=f"ocr_traduccion_{uuid.uuid4().hex[:8]}.mp3",
                mime="audio/mpeg"
            )
