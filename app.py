import streamlit as st

st.set_page_config(
    page_title="Toolkit AV/AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS: paleta elegante (rosado claro, dorado, nude) y tarjetas limpias
st.markdown(
    """
    <style>
    :root{
      --bg:#fffaf9;
      --card:#fff;
      --muted:#7c6b62;
      --accent1:#f7d6d9; /* rosado claro */
      --accent2:#e8d8c3; /* nude/dorado suave */
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
    .stButton>button {
      border-radius: 10px;
    }
    .card {
      background: var(--card);
      padding: 18px;
      border-radius: 12px;
      box-shadow: 0 6px 18px rgba(43,43,43,0.06);
      margin-bottom: 18px;
    }
    .small {
      color: var(--muted);
      font-size:14px;
    }
    .banner {
      border-radius: 12px;
      padding: 24px;
      background: linear-gradient(90deg, rgba(247,214,217,0.6), rgba(232,216,195,0.6));
      display:flex;
      align-items:center;
      gap:24px;
      margin-bottom:18px;
    }
    .title {
      font-size:28px;
      margin:0;
      color:#2b2b2b;
      font-weight:700;
    }
    .subtitle {
      margin:4px 0 0 0;
      color: #5b4f49;
    }
    .index-list li { margin-bottom:8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Navegación lateral
st.sidebar.title("Navegación")
pages = {
    "Inicio": "Inicio",
    "Texto → Audio (gTTS)": "Texto → Audio (gTTS)",
    "Voz → Texto (Whisper)": "Voz → Texto (Whisper)",
    "OCR": "OCR (pytesseract)",
    "OCR → Audio (Traducción + TTS)": "OCR → Audio (Traducción + TTS)",
    "NLP (TextBlob & NLTK)": "NLP (TextBlob & NLTK)",
    "Detección de Objetos (YOLO)": "Detección de Objetos (YOLO)",
    "Reconocimiento de Gestos": "Reconocimiento de Gestos (Teachable Machine)",
    "Chatbot Documento (LLM)": "Chatbot Documento (LLM)",
    "Interpretación de Imágenes": "Interpretación de Imágenes",
}
page = st.sidebar.radio("", list(pages.values()), index=0)

# Contenido: Inicio
if page == "Inicio":
    st.markdown(
        """
        <div class="banner">
          <div style="flex:1">
            <h1 class="title">Toolkit AV/AI</h1>
            <p class="subtitle">Colección de herramientas para procesamiento de voz, texto e imagen. Interfaz modular, diseño limpio, navegación lateral para acceder a cada herramienta.</p>
          </div>
          <div style="width:220px; text-align:center">
            <!-- SVG simple integrado para mantener el proyecto autónomo -->
            <svg width="200" height="120" viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="banner">
              <defs>
                <linearGradient id="g1" x1="0" x2="1">
                  <stop offset="0" stop-color="#F7D6D9"/>
                  <stop offset="1" stop-color="#E8D8C3"/>
                </linearGradient>
              </defs>
              <rect rx="14" width="200" height="120" fill="url(#g1)"/>
              <g transform="translate(18,22)" fill="#6b4f46" font-family="sans-serif">
                <text x="0" y="20" font-size="18" font-weight="700">AV · AI</text>
                <text x="0" y="44" font-size="12">Voz · Texto · Imagen</text>
                <text x="0" y="68" font-size="10" fill="#5b4f49">Navegación lateral</text>
              </g>
            </svg>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Descripción general")
    st.markdown(
        "Toolkit AV/AI reúne herramientas para convertir texto a audio, voz a texto, extraer texto de imágenes (OCR), combinar OCR con TTS y traducción, análisis de lenguaje natural con TextBlob/NLTK, detección de objetos con YOLO, reconocimiento de gestos mediante modelos exportados de Teachable Machine, un chatbot especializado para documentos (LLM) e interpretación detallada de imágenes."
    )
    st.markdown('<div class="small">Interfaz: navegación lateral. Cada página implementará carga/entrada, parámetros relevantes y salidas reproducibles / descargables.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Índice de funciones (acceso desde la barra lateral)")
    st.markdown(
        """
        <ul class="index-list">
          <li><strong>Texto → Audio (gTTS)</strong>: caja de texto para generar audio reproducible y descargable.</li>
          <li><strong>Voz → Texto (Whisper)</strong>: subir o grabar audio; detección de idioma; opción de elegir idioma de salida.</li>
          <li><strong>OCR</strong>: subir imagen/PDF; extracción de texto digital editable.</li>
          <li><strong>OCR → Audio</strong>: OCR + traducción a idioma seleccionado + audio descargable.</li>
          <li><strong>NLP (TextBlob & NLTK)</strong>: análisis de sentimiento y subjetividad, extracción de keywords, TF-IDF y preguntas sobre el texto (si no hay respuesta, mostrar error instructivo).</li>
          <li><strong>Detección de Objetos (YOLO)</strong>: subir imagen; devolver imagen con bounding boxes y etiquetas.</li>
          <li><strong>Reconocimiento de Gestos</strong>: detector en tiempo real con webcam usando modelo exportado desde Teachable Machine, y detector por foto.</li>
          <li><strong>Chatbot Documento (LLM)</strong>: cargar PDF; índice semántico; consultar sobre el contenido.</li>
          <li><strong>Interpretación de Imágenes</strong>: descripción detallada generada a partir de la imagen; posibilidad de hacer preguntas sobre la descripción.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Estado actual")
    st.markdown("Página de inicio implementada. Seleccione en la barra lateral la herramienta a desarrollar. Cada página se construirá completa y funcional antes de pasar a la siguiente.")
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Páginas con contenido inicial/plan y placeholders funcionales
    st.header(page)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if page == "Texto → Audio (gTTS)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: caja de texto libre.\n- Salida: reproducción inmediata y descarga del archivo .mp3 generado con gTTS.\n- Opciones: selección de voz/idioma y velocidad."
        )
        st.markdown("Estado: pendiente de implementación. Página preparada para recibir la implementación completa al recibir la siguiente instrucción.")
    elif page == "Voz → Texto (Whisper)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: subir audio o grabar desde micrófono.\n- Salida: transcripción con detección automática de idioma y opción de seleccionar idioma de salida.\n- Nota: posible descarga del .txt con la transcripción."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "OCR (pytesseract)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: imagen o PDF.\n- Salida: texto digital extraído (editable y descargable).\n- Opciones: seleccionar idioma de OCR."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "OCR → Audio (Traducción + TTS)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Flujo: OCR → traducción al idioma elegido → TTS (generación de audio reproducible y descargable).\n- Opciones: elegir voz y velocidad."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "NLP (TextBlob & NLTK)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: texto o documento.\n- Salidas: análisis de sentimiento y subjetividad, extracción de keywords, TF-IDF, búsqueda de respuestas (QA básica) con manejo de 'no encontrado'."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "Detección de Objetos (YOLO)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: imagen o vídeo corto.\n- Salida: imagen con bounding boxes, etiquetas y puntajes; opción para descargar imagen anotada."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "Reconocimiento de Gestos (Teachable Machine)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Detector en tiempo real vía webcam usando modelo exportado desde Teachable Machine.\n- Detector a partir de fotografía."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "Chatbot Documento (LLM)":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Cargar PDF, crear índice semántico, consultas en lenguaje natural sobre el documento, manejo de respuestas fuera del alcance."
        )
        st.markdown("Estado: pendiente de implementación.")
    elif page == "Interpretación de Imágenes":
        st.markdown("Funcionalidad prevista:")
        st.markdown(
            "- Entrada: imagen.\n- Salida: descripción detallada, lista de elementos detectados y posibilidad de hacer preguntas sobre la descripción."
        )
        st.markdown("Estado: pendiente de implementación.")
    st.markdown("</div>", unsafe_allow_html=True)
