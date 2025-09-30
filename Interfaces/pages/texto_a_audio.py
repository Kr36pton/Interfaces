import streamlit as st
import io




def app():
st.header("Texto → Audio (gTTS)")
st.markdown("Esta herramienta genera un archivo de audio MP3 a partir del texto ingresado.")


text = st.text_area("Introduce el texto a convertir", height=200)
lang = st.selectbox("Idioma (código)", ["es", "en", "fr", "de", "pt", "it"], index=0)


if st.button("Generar audio"):
if not text.strip():
st.error("Ingrese texto para generar el audio.")
return
try:
from gtts import gTTS


mp3_fp = io.BytesIO()
tts = gTTS(text, lang=lang)
tts.write_to_fp(mp3_fp)
mp3_fp.seek(0)


st.audio(mp3_fp, format="audio/mp3")
st.download_button("Descargar MP3", data=mp3_fp, file_name="tts.mp3", mime="audio/mp3")
except Exception as e:
st.error(f"Error generando audio: {e}")
st.info("Si aparece un error de importación, instale las dependencias desde requirements.txt.")
