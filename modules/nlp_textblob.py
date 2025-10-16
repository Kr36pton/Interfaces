import streamlit as st
from textblob import TextBlob
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Descargar recursos NLTK requeridos
for resource in ["punkt", "punkt_tab", "stopwords"]:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource)

from nltk.corpus import stopwords

def preprocess(text):
    text = re.sub(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s]", "", text.lower())
    tokens = nltk.word_tokenize(text)
    stop_words = set(stopwords.words("spanish") + stopwords.words("english"))
    filtered = [w for w in tokens if w not in stop_words and len(w) > 2]
    return filtered

def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    return sentiment, subjectivity

def extract_keywords(text, n=10):
    stoplist = stopwords.words("spanish") + stopwords.words("english")
    vectorizer = TfidfVectorizer(stop_words=stoplist)
    X = vectorizer.fit_transform([text])
    scores = zip(vectorizer.get_feature_names_out(), X.toarray()[0])
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return [word for word, score in sorted_scores[:n]]

def word_frequency(text, n=10):
    tokens = preprocess(text)
    freq = nltk.FreqDist(tokens)
    return freq.most_common(n)

def question_retrieval(text, question, threshold=0.35):
    sentences = nltk.sent_tokenize(text)
    corpus = [question] + sentences
    stoplist = stopwords.words("spanish") + stopwords.words("english")
    vectorizer = TfidfVectorizer(stop_words=stoplist)
    X = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(X[0:1], X[1:]).flatten()
    best_idx = np.argmax(sims)
    best_score = sims[best_idx]
    if best_score < threshold:
        return None, best_score
    return sentences[best_idx], best_score

def render():
    st.title("Procesamiento de Lenguaje Natural — TextBlob / NLTK")
    st.markdown("Analiza textos: **sentimiento**, **keywords**, **frecuencia** y **preguntas contextuales**.")

    text = st.text_area("Introduce el texto a analizar", height=250)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        run_sent = st.button("Sentimiento")
    with col2:
        run_keywords = st.button("Keywords (TF-IDF)")
    with col3:
        run_freq = st.button("Frecuencia")
    with col4:
        run_question = st.button("Pregunta")

    if not text.strip():
        st.info("Introduce un texto para comenzar.")
        return

    if run_sent:
        with st.spinner("Analizando sentimiento..."):
            polarity, subjectivity = analyze_sentiment(text)
        st.subheader("Resultado de Sentimiento")
        st.write(f"Polaridad: **{polarity:.3f}** (−1 negativo, +1 positivo)")
        st.write(f"Subjetividad: **{subjectivity:.3f}** (0 objetiva, 1 subjetiva)")
        if polarity > 0:
            st.success("Sentimiento positivo")
        elif polarity < 0:
            st.error("Sentimiento negativo")
        else:
            st.warning("Sentimiento neutro")

    if run_keywords:
        with st.spinner("Extrayendo palabras clave..."):
            keywords = extract_keywords(text)
        st.subheader("Palabras clave principales")
        st.write(", ".join(keywords))

    if run_freq:
        with st.spinner("Analizando frecuencia..."):
            freq = word_frequency(text)
        st.subheader("Palabras más frecuentes")
        for word, count in freq:
            st.write(f"{word}: {count}")

    if run_question:
        question = st.text_input("Escribe tu pregunta sobre el texto:")
        if question:
            with st.spinner("Buscando respuesta..."):
                answer, score = question_retrieval(text, question)
            if answer:
                st.subheader("Respuesta encontrada")
                st.markdown(f"**Fragmento:** {answer}")
                st.caption(f"(Similitud: {score:.2f})")
            else:
                st.warning("No se encontró una respuesta clara. Reformula la pregunta.")
