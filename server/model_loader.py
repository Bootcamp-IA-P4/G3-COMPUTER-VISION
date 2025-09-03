# server/model_loader.py

import os
from ultralytics import YOLO

# Variable global para el modelo cargado
model = None


def load_model(model_path: str = "models/best.pt"):
    """
    Carga el modelo YOLO desde un archivo .pt
    """
    global model

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"No se encontró el modelo en {model_path}")

    model = YOLO(model_path)
    print(f"✅ Modelo cargado desde: {model_path}")
    return model


def get_model():
    """
    Devuelve el modelo cargado.
    Si aún no está cargado, lo intenta cargar con la ruta por defecto.
    """
    global model
    if model is None:
        model = load_model()
    return model
