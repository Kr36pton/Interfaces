import streamlit as st
from gtts import gTTS
import io
import uuid

def render():
    st.title("Texto → Audio (gTTS)")
    st.markdown("Convierte texto a audio (MP3).")

    # Opciones de idioma comunes
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
        text = st.text_area("Texto a convertir", height=240, placeholder="Escribe o pega el texto aquí...")
        cols = st.columns([1, 1, 1])
        with cols[0]:
            lang_label = st.selectbox("Idioma", list(LANGUAGES.keys()), index=0)
        with cols[1]:
            slow = st.checkbox("Reproducción lenta (slow)", value=False)
        with cols[2]:
            filename_input = st.text_input("Nombre de archivo (sin extensión)", value="audio")
        submit = st.form_submit_button("Generar audio")

    if submit:
        if not text or text.strip() == "":
            st.error("El texto está vacío. Inserta texto para generar audio.")
            return

        # Preparar texto sencillo
        cleaned_text = text.strip()
        lang_code = LANGUAGES[lang_label]

        # Generar con gTTS en memoria
        try:
            tts = gTTS(text=cleaned_text, lang=lang_code, slow=slow)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
        except Exception as e:
            st.error(f"Error al generar audio: {e}")
            return

        # Reproducción en la app
        st.audio(mp3_fp.getvalue())

        # Preparar nombre de archivo único si el usuario no quiere sobrescribir
        safe_name = filename_input.strip() if filename_input.strip() != "" else "audio"
        unique_name = f"{safe_name}_{uuid.uuid4().hex[:8]}.mp3"

        # Botón de descarga
        st.download_button(
            label="Descargar MP3",
            data=mp3_fp.getvalue(),
            file_name=unique_name,
            mime="audio/mpeg",
        )

        # Mostrar tamaño y meta información
        size_kb = len(mp3_fp.getvalue()) / 1024
        st.markdown(f"**Tamaño:** {size_kb:.1f} KB — **Idioma:** {lang_label} — **Velocidad:** {'lenta' if slow else 'normal'}")
