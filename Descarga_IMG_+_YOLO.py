import os
import re
import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from PIL import Image

# Ruta al Excel
file_path = "logotipos_limpios.xlsx"

# Cargar dataset
df = pd.ExcelFile(file_path)
data = pd.read_excel(file_path, sheet_name="Sheet1")

# Carpeta base
output_dir = Path("dataset_logos")
output_dir.mkdir(parents=True, exist_ok=True)

# Carpetas YOLO
yolo_images = Path("dataset_yolo/images")
yolo_labels = Path("dataset_yolo/labels")
yolo_images.mkdir(parents=True, exist_ok=True)
yolo_labels.mkdir(parents=True, exist_ok=True)

# Función para limpiar nombre
def clean_brand_name(name):
    if pd.isna(name):
        return "Desconocido"
    return re.sub(r"S\.Net.*", "", str(name)).strip()

# Crear lista de clases
brands = sorted(set(clean_brand_name(b) for b in data["Nombre de Marca"]))
brand_to_id = {brand: idx for idx, brand in enumerate(brands)}

# Guardar archivo de clases (YOLO)
with open("dataset_yolo/classes.txt", "w", encoding="utf-8") as f:
    for brand in brands:
        f.write(brand + "\n")

errors = []

for idx, row in tqdm(data.iterrows(), total=len(data)):
    url = row["URL del Logotipo"]
    brand = clean_brand_name(row["Nombre de Marca"])
    class_id = brand_to_id[brand]

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            file_ext = url.split(".")[-1].lower()
            if file_ext not in ["jpg", "jpeg", "png", "webp"]:
                file_ext = "jpg"
            img_name = f"{brand}_{idx}.{file_ext}"
            img_path = yolo_images / img_name

            # Guardar imagen
            with open(img_path, "wb") as f:
                f.write(response.content)

            # Abrir imagen para dimensiones
            with Image.open(img_path) as img:
                w, h = img.size

            # YOLO format: class_id cx cy w h (normalizado 0-1)
            cx, cy = 0.5, 0.5  # logo centrado
            bw, bh = 1.0, 1.0  # caja cubre toda la imagen

            label_path = yolo_labels / (img_name.replace(file_ext, "txt"))
            with open(label_path, "w") as f:
                f.write(f"{class_id} {cx} {cy} {bw} {bh}\n")

        else:
            errors.append((idx, url, "Bad status"))
    except Exception as e:
        errors.append((idx, url, str(e)))

print("Descarga completada con", len(errors), "errores")
print("Total clases:", len(brands))
