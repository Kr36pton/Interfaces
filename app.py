import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="📦",  # corregido: el emoji debe ir entre comillas
    layout="wide"
)

# Estilos y ocultar el menú nativo de Streamlit
st.markdown(
    """
    <style>
    section[data-testid="stSidebarNav"] {display: none;}
    :root{
        --bg:#fffaf8;
        --card:#fff;
        --accent:#f7d6e0;
        --muted:#bfa6a0;
        --gold:#cfa46b;
    }
    .reportview-container, .main{background: var(--bg);}
    header {background: linear-gradient(90deg, rgba(247,214,224,0.25), rgba(255,250,245,0.5));}
    .stSidebar .css-1d391kg {width: 270px;}
    .page-card {
        background: var(--card);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mapeo de páginas
PAGES = {
    "Inicio": "modules.inicio",
    "Texto → Audio (gTTS)": "modules.texto_a_audio",
    "Voz → Texto (Vosk)": "modules.voz_a_texto",
}

with st.sidebar:
    st.title("Navegación")
    choice = st.radio("", list(PAGES.keys()), index=0)

# Importar módulo
module_path = PAGES[choice]
try:
    page = importlib.import_module(module_path)
    if hasattr(page, "render"):
        page.render()
    else:
        st.error(f"El módulo {module_path} existe pero no define `render()`.")
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
