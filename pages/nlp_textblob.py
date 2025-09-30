import streamlit as st

def render():
    st.title("NLP: Sentimiento, TF-IDF y Palabras clave")
    st.markdown("Página en desarrollo. Funcionalidad prevista:")
    st.markdown("""
- Entrada: texto o archivo.
- Análisis: sentimiento y subjetividad (TextBlob), extracción de frases sustantivas, TF-IDF y palabras clave.
- QA interno: preguntar sobre el texto; si no hay respuesta, devolver mensaje claro.
    """)
