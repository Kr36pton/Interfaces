import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import io
import torch
import cv2

from ultralytics import YOLO

@st.cache_resource(show_spinner=False)
def load_model(model_name: str):
    model = YOLO(model_name)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    return model, device

def bgr_to_rgb(img_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

def results_to_dataframe(res) -> pd.DataFrame:
    boxes = res.boxes
    if boxes is None or boxes.data is None or len(boxes) == 0:
        return pd.DataFrame(columns=["clase", "confianza", "x1", "y1", "x2", "y2"])
    xyxy = boxes.xyxy.cpu().numpy()
    cls = boxes.cls.cpu().numpy().astype(int)
    conf = boxes.conf.cpu().numpy()
    names = res.names
    rows = []
    for i in range(len(xyxy)):
        x1, y1, x2, y2 = xyxy[i]
        rows.append({
            "clase": names.get(cls[i], str(cls[i])),
            "confianza": float(conf[i]),
            "x1": float(x1), "y1": float(y1), "x2": float(x2), "y2": float(y2)
        })
    df = pd.DataFrame(rows)
    df.sort_values(by="confianza", ascending=False, inplace=True, ignore_index=True)
    return df

def render():
    st.title("Identificación de objetos (YOLOv8)")

    col_top = st.columns([2, 1, 1])
    with col_top[0]:
        uploaded = st.file_uploader("Sube una imagen (JPG/PNG/WebP/BMP)", type=["jpg", "jpeg", "png", "webp", "bmp"])
    with col_top[1]:
        model_choice = st.selectbox(
            "Modelo",
            options=["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"],
            index=0,
            help="Modelos más pequeños a más grandes. 'n' es el más rápido, 'm' es más preciso."
        )
    with col_top[2]:
        conf_th = st.slider("Umbral de confianza", 0.05, 0.95, 0.25, 0.05)

    detect = st.button("Detectar", use_container_width=True)

    if uploaded is None:
        return

    image = Image.open(uploaded).convert("RGB")
    st.image(image, caption="Imagen de entrada", use_container_width=True)

    if not detect:
        return

    with st.spinner("Cargando modelo y ejecutando inferencia..."):
        model, device = load_model(model_choice)
        # Ultralytics acepta arrays NumPy RGB directamente
        img_np = np.array(image)
        results = model.predict(img_np, conf=conf_th, verbose=False)

    if not results or len(results) == 0:
        st.error("No se obtuvieron resultados del modelo.")
        return

    res = results[0]

    # Imagen anotada
    plotted_bgr = res.plot()  # Devuelve BGR
    plotted_rgb = bgr_to_rgb(plotted_bgr)
    out_img = Image.fromarray(plotted_rgb)

    st.subheader("Resultado")
    st.image(out_img, caption="Detecciones", use_container_width=True)

    # Tabla de detecciones
    df = results_to_dataframe(res)
    st.subheader("Objetos detectados")
    if df.empty:
        st.info("Sin detecciones por encima del umbral.")
    else:
        st.dataframe(df, use_container_width=True)

    # Descarga de imagen anotada
    buf = io.BytesIO()
    out_img.save(buf, format="PNG")
    buf.seek(0)

    st.download_button(
        label="Descargar imagen con detecciones",
        data=buf.getvalue(),
        file_name="detecciones_yolo.png",
        mime="image/png",
        use_container_width=True
    )
