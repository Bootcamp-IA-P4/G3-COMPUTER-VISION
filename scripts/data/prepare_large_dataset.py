
import pandas as pd
from pathlib import Path
import requests
import os
import re
import sys
import subprocess
import yaml
from tqdm import tqdm

# --- VERIFICACIÓN E INSTALACIÓN DE DEPENDENCIAS ---
def install_package(package):
    """Instala un paquete usando pip."""
    print(f"La librería '{package}' es necesaria. Instalando...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar {package}: {e}")
        print("Por favor, instala el paquete manualmente y vuelve a ejecutar el script.")
        sys.exit(1)

try:
    import openpyxl
except ImportError:
    install_package("openpyxl")

try:
    import tqdm
except ImportError:
    install_package("tqdm")


# --- CONFIGURACIÓN ---
XLSX_FILE_PATH = Path("data/logotipos_limpios.xlsx")
OUTPUT_DATASET_PATH = Path("data/datasets/dataset_large")
URL_COLUMN = "URL del Logotipo"
BRAND_COLUMN = "Nombre de Marca"

# --- FUNCIONES ---

def sanitize_filename(name):
    """Limpia un string para que sea un nombre de archivo válido."""
    name = str(name).lower()
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'[^a-z0-9_.-]', '', name)
    return name

def create_dirs():
    """Crea los directorios de salida para imágenes y etiquetas."""
    (OUTPUT_DATASET_PATH / "images").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DATASET_PATH / "labels").mkdir(parents=True, exist_ok=True)
    print(f"Directorios creados en: {OUTPUT_DATASET_PATH}")

def process_dataset():
    """Función principal para procesar el excel, descargar imágenes y crear etiquetas."""
    if not XLSX_FILE_PATH.exists():
        print(f"Error: No se encuentra el archivo de entrada: {XLSX_FILE_PATH}")
        return

    df = pd.read_excel(XLSX_FILE_PATH)
    
    unique_brands = df[BRAND_COLUMN].dropna().unique()
    class_map = {brand: i for i, brand in enumerate(unique_brands)}
    
    print(f"Se encontraron {len(unique_brands)} marcas únicas.")

    brand_counters = {brand: 0 for brand in unique_brands}

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Procesando imágenes"):
        brand_name = row[BRAND_COLUMN]
        image_url = row[URL_COLUMN]

        if pd.isna(brand_name) or not isinstance(image_url, str) or not image_url.startswith('http'):
            # print(f"Fila {index} inválida (URL o marca vacía). Saltando.")
            continue

        class_id = class_map[brand_name]
        
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # print(f"Error descargando {image_url}. Saltando.")
            continue

        content_type = response.headers.get('content-type')
        if 'image' not in content_type:
            # print(f"URL no es una imagen: {image_url}. Saltando.")
            continue
            
        file_extension = Path(image_url).suffix.split('?')[0] or '.jpg'
        if len(file_extension) > 5: # Evitar extensiones raras
            file_extension = '.jpg'

        sanitized_brand = sanitize_filename(brand_name)
        current_index = brand_counters[brand_name]
        file_stem = f"{sanitized_brand}_{current_index}"
        
        image_filename = file_stem + file_extension
        label_filename = file_stem + ".txt"
        
        brand_counters[brand_name] += 1

        with open(OUTPUT_DATASET_PATH / "images" / image_filename, 'wb') as f:
            f.write(response.content)

        with open(OUTPUT_DATASET_PATH / "labels" / label_filename, 'w') as f:
            f.write(f"{class_id} 0.5 0.5 1.0 1.0")

    print("\nProceso de descarga y anotación completado.")

    yaml_data = {
        'path': str(OUTPUT_DATASET_PATH.resolve()),
        'train': 'images',
        'val': 'images',
        'nc': len(unique_brands),
        'names': [str(b) for b in unique_brands]
    }

    yaml_path = OUTPUT_DATASET_PATH / "data.yaml"
    with open(yaml_path, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"Archivo data.yaml creado en: {yaml_path}")

# --- EJECUCIÓN ---
if __name__ == "__main__":
    create_dirs()
    process_dataset()
