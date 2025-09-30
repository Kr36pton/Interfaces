import streamlit as st
from gtts import gTTS
import io
import tempfile
import base64

st.set_page_config(
    page_title="Texto → Audio (gTTS)",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS (mismo estilo que app.py)
st.markdown(
    """
    <style>
    :root{
      --bg:#fffaf9;
      --card:#fff;
      --muted:#7c6b62;
      --accent1:#f7d6d9;
      --accent2:#e8d8c3;
      --accent3:#f2e9e1;
    }
    html,body,#root, .stApp { background: var(--bg); color: #2b2b2b; font-family: "Inter", "Segoe UI", Roboto, sans-serif; }
    .sidebar .sidebar-content { background: linear-gradient(180deg, var(--accent1), var(--accent2)); padding: 18px 12px; border-radius: 12px; }
    .stButton>button { border-radius: 10px; }
    .card { background: var(--card); padding: 18px; border-radius: 12px; box-shadow: 0 6px 18px rgba(43,43,43,0.06); margin-bottom: 18px; }
    .small { color: var(--muted); font-size:14px; }
    .title { font-size:22px; margin:0; color:#2b2b2b; font-weight:700; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Barra lateral informativa y navegación consistente
st.sidebar.title("Herramientas")
st.sidebar.markdown(
    """
    - Inicio\n- Texto → Audio (gTTS)\n- Voz → Texto (Whisper)\n- OCR\n- OCR → Audio\n- NLP\n- Detección de Objetos\n- Reconocimiento de Gestos\n- Chatbot Documento\n- Interpretación de Imágenes
    """
)

# Contenedor principal
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("## Texto → Audio (gTTS)")
st.markdown("Ingrese texto, elija idioma y velocidad. Genere y descargue el archivo MP3 resultante.")
st.markdown("</div>", unsafe_allow_html=True)

# Inputs
with st.form("gtts_form"):
    text = st.text_area("Texto a convertir en audio", height=200, placeholder="Escriba o pegue el texto aquí...")
    col1, col2 = st.columns([2,1])
    with col1:
        # Idiomas disponibles según gTTS
        from gtts.lang import tts_langs
        langs = tts_langs()
        # Ordenamos por código para estabilidad
        lang_options = sorted(langs.items(), key=lambda x: x[0])
        lang_code = st.selectbox("Idioma (código)", options=[k for k,_ in lang_options], index=0, format_func=lambda k: f"{k} — {langs[k]}")
    with col2:
        slow = st.checkbox("Lento (slow)", value=False)
        filename = st.text_input("Nombre archivo (sin extensión)", value="audio_gtts")
    submit = st.form_submit_button("Generar audio")

if submit:
    if not text.strip():
        st.error("El texto está vacío. Ingrese texto para generar audio.")
    else:
        try:
            tts = gTTS(text=text, lang=lang_code, slow=slow)
            mp3_bytes_io = io.BytesIO()
            tts.write_to_fp(mp3_bytes_io)
            mp3_bytes = mp3_bytes_io.getvalue()

            st.audio(mp3_bytes, format="audio/mp3")

            b64 = base64.b64encode(mp3_bytes).decode()
            href = f"data:audio/mp3;base64,{b64}"
            st.download_button(
                label="Descargar MP3",
                data=mp3_bytes,
                file_name=f"{filename}.mp3",
                mime="audio/mpeg",
            )
            st.success("Audio generado correctamente.")
        except Exception as e:
            st.error(f"Error generando audio: {e}")
