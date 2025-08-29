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

# Modificar la estructura de carpetas YOLO
def create_brand_folders(brands, base_path):
    for brand in brands:
        brand_folder = base_path / brand
        brand_folder.mkdir(parents=True, exist_ok=True)
    return base_path

# Modificar la parte de las carpetas YOLO
yolo_base = Path("dataset_yolo")
yolo_images = yolo_base / "images"
yolo_labels = yolo_base / "labels"

# Crear carpetas base
yolo_base.mkdir(parents=True, exist_ok=True)
yolo_images.mkdir(parents=True, exist_ok=True)
yolo_labels.mkdir(parents=True, exist_ok=True)

# Función para limpiar nombre
def clean_brand_name(name):
    if pd.isna(name):
        return "Desconocido"
    
    # Convertir a string y limpiar espacios
    name = str(name).strip()
    
    # Palabras a remover
    remove_words = [
        'Vector', 'Download', 'Eps', 'Black', 'Logo', 'Brand', 
        'Preview', 'Current', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]
    
    # Remover números al inicio
    name = re.sub(r'^\d+\s*', '', name)
    
    # Remover palabras innecesarias
    for word in remove_words:
        name = re.sub(rf'\s*{word}\s*', ' ', name, flags=re.IGNORECASE)
    
    # Limpiar caracteres especiales
    name = re.sub(r'[^\w\s-]', '', name)
    
    # Remover espacios múltiples
    name = re.sub(r'\s+', ' ', name)
    
    # Capitalizar cada palabra
    name = ' '.join(word.capitalize() for word in name.split())
    
    return name.strip()

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
                
            # Crear nombre de archivo y rutas
            img_name = f"{brand}_{idx}.{file_ext}"
            brand_images_dir = yolo_images / brand
            brand_labels_dir = yolo_labels / brand
            
            # Crear carpetas si no existen
            brand_images_dir.mkdir(parents=True, exist_ok=True)
            brand_labels_dir.mkdir(parents=True, exist_ok=True)
            
            img_path = brand_images_dir / img_name

            # Guardar imagen
            with open(img_path, "wb") as f:
                f.write(response.content)

            # Abrir imagen para dimensiones
            with Image.open(img_path) as img:
                w, h = img.size

            # YOLO format: class_id cx cy w h (normalizado 0-1)
            cx, cy = 0.5, 0.5
            bw, bh = 1.0, 1.0

            # Guardar etiqueta en la subcarpeta correspondiente
            label_path = brand_labels_dir / (img_name.replace(file_ext, "txt"))
            with open(label_path, "w") as f:
                f.write(f"{class_id} {cx} {cy} {bw} {bh}\n")

        else:
            errors.append((idx, url, "Bad status"))
    except Exception as e:
        errors.append((idx, url, str(e)))

print("Descarga completada con", len(errors), "errores")
print("Total clases:", len(brands))
