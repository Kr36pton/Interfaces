import streamlit as st
from gtts import gTTS
import io
import uuid

def render():
    st.title("Texto → Audio (gTTS)")
    st.markdown("Convierte texto en audio reproducible (MP3).")

    LANGUAGES = {
        "Español (es)": "es",
        "Inglés (en)": "en",
        "Francés (fr)": "fr",
        "Portugués (pt)": "pt",
        "Italiano (it)": "it",
        "Alemán (de)": "de",
        "Holandés (nl)": "nl",
    }

    with st.form(key="tts_form"):
        text = st.text_area("Texto a convertir", height=200)
        lang_label = st.selectbox("Idioma", list(LANGUAGES.keys()), index=0)
        slow = st.checkbox("Velocidad lenta", value=False)
        filename_input = st.text_input("Nombre de archivo (sin extensión)", value="audio")
        submit = st.form_submit_button("Generar audio")

    if submit:
        if not text.strip():
            st.error("El texto está vacío.")
            return

        lang_code = LANGUAGES[lang_label]
        try:
            tts = gTTS(text=text.strip(), lang=lang_code, slow=slow)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
        except Exception as e:
            st.error(f"Error al generar audio: {e}")
            return

        st.audio(mp3_fp.getvalue())

        safe_name = filename_input.strip() if filename_input.strip() else "audio"
        unique_name = f"{safe_name}_{uuid.uuid4().hex[:8]}.mp3"

        st.download_button(
            label="Descargar MP3",
            data=mp3_fp.getvalue(),
            file_name=unique_name,
            mime="audio/mpeg",
        )
