import streamlit as st
import io
import os
import zipfile
import requests
import json
import wave
import tempfile
from pathlib import Path

# Reconocimiento offline: Vosk
try:
    from vosk import Model, KaldiRecognizer
except Exception as e:
    st.error("La librería 'vosk' no está disponible. Añade 'vosk' en requirements.txt e instala dependencias.")
    raise

# Grabación en navegador
try:
    from audiorecorder import audiorecorder
except Exception:
    audiorecorder = None  # no crítico, solo desactivar la grabación si falta

MODELS = {
    "en": {
        "name": "vosk-model-small-en-us-0.15",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip",
    },
    "es": {
        "name": "vosk-model-small-es-0.42",
        "url": "https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip",
    },
}

MODEL_BASE_DIR = Path("models")


def ensure_model(lang_code: str):
    """
    Asegura que el modelo Vosk para el idioma exista en disk.
    Si no existe, intenta descargar y descomprimir el ZIP oficial.
    """
    if lang_code not in MODELS:
        raise ValueError("Idioma no soportado para modelo offline.")

    info = MODELS[lang_code]
    model_dir = MODEL_BASE_DIR / info["name"]
    if model_dir.exists():
        return str(model_dir)

    MODEL_BASE_DIR.mkdir(parents=True, exist_ok=True)
    zip_url = info["url"]
    tmp_zip = MODEL_BASE_DIR / f"{info['name']}.zip"

    # Descargar con progreso
    with st.spinner(f"Descargando modelo Vosk ({lang_code}) — esto puede tardar varios minutos"):
        resp = requests.get(zip_url, stream=True, timeout=60)
        resp.raise_for_status()
        total = int(resp.headers.get("content-length", 0))
        chunk_size = 32768
        with open(tmp_zip, "wb") as fh:
            prog = st.progress(0)
            downloaded = 0
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if not chunk:
                    break
                fh.write(chunk)
                downloaded += len(chunk)
                if total:
                    prog.progress(min(100, int(downloaded * 100 / total)))
    # Descomprimir
    with st.spinner("Descomprimiendo modelo..."):
        with zipfile.ZipFile(tmp_zip, "r") as zf:
            zf.extractall(MODEL_BASE_DIR)
    tmp_zip.unlink(missing_ok=True)
    if not model_dir.exists():
        # A veces el zip contiene una carpeta con nombre diferente; intentar detectar carpeta extraída
        # Buscar la carpeta más grande creada dentro de models/
        candidates = [p for p in MODEL_BASE_DIR.iterdir() if p.is_dir()]
        if candidates:
            # elegir el más reciente
            candidates_sorted = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)
            model_dir = candidates_sorted[0]
    return str(model_dir)


@st.cache_resource(show_spinner=False)
def load_vosk_model(lang_code: str):
    path = ensure_model(lang_code)
    return Model(path)


def read_wav_bytes_to_wave_reader(wav_bytes: bytes):
    """
    Devuelve un objeto wave.Wave_read que lee desde bytes en memoria.
    """
    bio = io.BytesIO(wav_bytes)
    try:
        wf = wave.open(bio, "rb")
    except wave.Error as e:
        raise ValueError("El archivo no es un WAV PCM válido o está corrupto.") from e
    return wf


def transcribe_with_vosk(model, wf):
    """
    Ejecuta la transcripción con KaldiRecognizer leyendo frames desde wave.Wave_read.
    Devuelve el texto completo (concatenado).
    """
    sample_rate = wf.getframerate()
    rec = KaldiRecognizer(model, sample_rate)
    rec.SetWords(True)
    final_text = []
    # Leer en trozos
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            text = res.get("text", "").strip()
            if text:
                final_text.append(text)
    # Resultado final
    final_res = json.loads(rec.FinalResult())
    if final_res.get("text"):
        final_text.append(final_res.get("text", "").strip())
    return " ".join(final_text).strip()


def render():
    st.title("Voz → Texto (Reconocimiento offline con Vosk)")
    st.markdown(
        "Transcripción offline. **Requisitos**: solo archivos WAV PCM o grabaciones desde el navegador (WAV). "
        "Si no existe el modelo para el idioma seleccionado, el sistema lo descargará automáticamente."
    )

    # Opciones de idioma / modelo
    col_a, col_b = st.columns([2, 1])
    with col_a:
        lang = st.selectbox("Idioma de entrada (voz)", ["es", "en"], index=0)
    with col_b:
        mode = st.selectbox("Acción", ["Transcribir", "Traducir"], index=0)

    # Mostrar selector de idioma destino solo si Traducir
    target_lang = None
    if mode == "Traducir":
        target_lang = st.selectbox("Traducir a", ["en", "es", "fr", "de", "it", "pt"], index=0)

    st.markdown("### Opción A — Subir archivo WAV (PCM 16-bit)")
    uploaded = st.file_uploader("Subir archivo WAV", type=["wav"])

    st.markdown("### Opción B — Grabar desde el navegador")
    audio = None
    if audiorecorder is not None:
        audio = audiorecorder("Grabar", "Detener")
        if audio and len(audio) > 0:
            st.audio(audio.tobytes(), format="audio/wav")
    else:
        st.info("Grabación en navegador no disponible porque falta 'streamlit-audiorecorder'.")

    # Procesar
    if st.button("Procesar"):
        # Obtener bytes
        wav_bytes = None
        if uploaded is not None:
            wav_bytes = uploaded.read()
        elif audio is not None and len(audio) > 0:
            wav_bytes = audio.tobytes()
        else:
            st.error("No se proporcionó audio. Suba un WAV o grabe desde el navegador.")
            return

        # Intentar cargar modelo y transcribir
        with st.spinner("Cargando modelo y transcribiendo..."):
            try:
                model = load_vosk_model(lang)
            except Exception as e:
                st.error(f"No se pudo cargar/descargar el modelo para '{lang}': {e}")
                return

            try:
                wf = read_wav_bytes_to_wave_reader(wav_bytes)
            except Exception as e:
                st.error(f"Error al leer WAV: {e}")
                return

            try:
                text = transcribe_with_vosk(model, wf)
            except Exception as e:
                st.error(f"Error durante la transcripción: {e}")
                return

        if not text:
            st.warning("No se detectó texto en el audio.")
            return

        st.markdown("#### Transcripción")
        st.text_area("Resultado", value=text, height=200)

        # Traducción opcional (usa API web de google translate a través de googletrans)
        translated_text = None
        if mode == "Traducir":
            try:
                from googletrans import Translator
                translator = Translator()
                tr = translator.translate(text, dest=target_lang)
                translated_text = tr.text
            except Exception as e:
                st.error(f"Error al traducir (se intentó con googletrans): {e}")
                translated_text = None

            if translated_text:
                st.markdown(f"#### Traducción → {target_lang}")
                st.text_area("Traducción", value=translated_text, height=160)

        # Botones de descarga
        st.download_button("Descargar transcripción (.txt)", data=text, file_name="transcripcion.txt", mime="text/plain")
        if translated_text:
            st.download_button("Descargar traducción (.txt)", data=translated_text, file_name="traduccion.txt", mime="text/plain")
