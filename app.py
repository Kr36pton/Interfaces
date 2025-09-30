import streamlit as st

st.set_page_config(
    page_title="Toolkit AV/AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS compartido (paleta: rosado claro, dorado, nude) y estilo limpio
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
    html,body,#root, .stApp {
      background: var(--bg);
      color: #2b2b2b;
      font-family: "Inter", "Segoe UI", Roboto, sans-serif;
    }
    .sidebar .sidebar-content {
      background: linear-gradient(180deg, var(--accent1), var(--accent2));
      padding: 18px 12px;
      border-radius: 12px;
    }
    .stButton>button { border-radius: 10px; }
    .card {
      background: var(--card);
      padding: 18px;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(43,43,43,0.06);
      margin-bottom: 18px;
    }
    .small { color: var(--muted); font-size:14px; }
    .banner {
      border-radius: 12px;
      padding: 24px;
      background: linear-gradient(90deg, rgba(247,214,217,0.6), rgba(232,216,195,0.6));
      display:flex; align-items:center; gap:24px; margin-bottom:18px;
    }
    .title { font-size:28px; margin:0; color:#2b2b2b; font-weight:700; }
    .subtitle { margin:4px 0 0 0; color: #5b4f49; }
    .index-list li { margin-bottom:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Barra lateral (informativa, consistencia entre páginas)
st.sidebar.title("Navegación (Pages)")
st.sidebar.markdown(
    """
    - Inicio (esta página)
    - Texto → Audio (gTTS)  — pages/01_texto_audio_gtts.py
    - Voz → Texto (Whisper) — pages/02_voz_texto_whisper.py
    - OCR — pages/03_ocr.py
    - OCR → Audio (Traducción + TTS) — pages/04_ocr_audio.py
    - NLP (TextBlob & NLTK) — pages/05_nlp.py
    - Detección de Objetos (YOLO) — pages/06_yolo.py
    - Reconocimiento de Gestos — pages/07_gestos.py
    - Chatbot Documento (LLM) — pages/08_chatbot_documento.py
    - Interpretación de Imágenes — pages/09_interpretacion_imagen.py

    Use la sección "Pages" de Streamlit (izquierda superior) para abrir cada archivo de página.
    """
)

# Contenido principal: descripción breve y guía de flujo de trabajo
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("## Toolkit AV/AI — Inicio")
st.markdown(
    "Colección modular de herramientas para procesamiento de voz, texto e imagen. Cada funcionalidad está implementada en su propio archivo dentro de la carpeta `pages/`. Abra la página deseada desde el panel lateral de Streamlit o desde el gestor de Pages de la aplicación."
)
st.markdown("### Flujo de trabajo")
st.markdown(
    "- Desarrollamos y probamos página por página.\n- Cada página es autocontenida: estilos, barra lateral consistente y funcionalidad completa.\n- Solicite la siguiente página cuando confirme que la actual cumple sus requisitos."
)
st.markdown("</div>", unsafe_allow_html=True)
