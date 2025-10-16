import streamlit as st
import importlib

st.set_page_config(
    page_title="Suite Multimedia — Herramientas IA",
    page_icon="🧰",
    layout="wide",
)

# Ocultar navegación nativa autogenerada
st.markdown(
    """
    <style>
      section[data-testid="stSidebarNav"] {display: none;}
      :root{ --bg:#fffaf8; --card:#ffffff; --muted:#8a7e79; }
      .stApp, .main { background: var(--bg); }
      .page-card { background: var(--card); border-radius:12px; padding:20px; box-shadow:0 1px 6px rgba(0,0,0,0.06); }
      .stButton>button { border-radius:10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Cada entrada puede listar varios módulos candidatos para tolerar estructuras distintas (modules/* o src/pages/*)
PAGES = {
    "Inicio": ["modules.inicio", "src.pages.inicio"],
    "Texto → Audio (gTTS)": ["modules.texto_a_audio", "src.pages.texto_a_audio"],
    "Voz → Texto (Vosk)": ["modules.voz_a_texto", "src.pages.voz_a_texto"],
    "OCR (Imagen → Texto)": ["modules.ocr", "src.pages.ocr"],
    "NLP: Sentimiento, TF-IDF y Palabras clave": ["modules.nlp_textblob", "src.pages.nlp_textblob"],
    "Identificación de objetos (YOLO)": ["modules.yolo_objetos", "src.pages.yolo_objetos"],
    "Identificación de gestos (Teachable Machine)": ["modules.gestos", "src.pages.gestos"],
    # Si en el futuro habilitas OCR → Traducción → Audio, añade aquí su ruta.
}

def import_first(candidates):
    last_err = None
    for name in candidates:
        try:
            return importlib.import_module(name)
        except ModuleNotFoundError as e:
            last_err = e
            continue
    raise last_err or ModuleNotFoundError(f"No se pudo importar ninguno de: {candidates}")

with st.sidebar:
    st.title("Navegación")
    choice = st.radio(
        "Selecciona una página:",
        list(PAGES.keys()),
        index=0,
        label_visibility="collapsed",  # evita warning de accesibilidad manteniendo la UI limpia
    )

module_candidates = PAGES[choice]
try:
    page_module = import_first(module_candidates)
    if hasattr(page_module, "render") and callable(page_module.render):
        page_module.render()
    else:
        st.error(f"El módulo seleccionado no define render(). Revisar: {module_candidates}")
except Exception as e:
    st.error(f"Error al cargar la página '{choice}': {e}")
