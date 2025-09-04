import os
import shutil
import yaml
from pathlib import Path

def copy_dataset(src_path, dest_path):
    """
    Copiar dataset a una nueva ubicación
    """
    src_path = Path(src_path)
    dest_path = Path(dest_path)
    
    # Crear directorio destino si no existe
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Copiar todo el contenido
    for item in src_path.glob('*'):
        if item.is_dir():
            shutil.copytree(item, dest_path / item.name)
        else:
            shutil.copy2(item, dest_path)
    
    return dest_path

def reindex_dataset(dataset_path, prefix):
    """
    Reindexar imágenes y etiquetas de un dataset
    """
    dataset_path = Path(dataset_path)
    
    # Directorios a procesar
    dirs = ['train', 'valid', 'test']
    
    for dir_name in dirs:
        images_dir = dataset_path / dir_name / 'images'
        labels_dir = dataset_path / dir_name / 'labels'
        
        if not images_dir.exists() or not labels_dir.exists():
            continue
            
        # Obtener lista de imágenes
        image_files = list(images_dir.glob('*.jpg'))
        
        # Renombrar imágenes y sus etiquetas correspondientes
        for idx, img_path in enumerate(sorted(image_files)):
            # Nuevo nombre de archivo
            new_name = f"{prefix}_{idx:06d}"
            
            # Renombrar imagen
            new_img_path = images_dir / f"{new_name}.jpg"
            img_path.rename(new_img_path)
            
            # Renombrar etiqueta correspondiente
            label_path = labels_dir / f"{img_path.stem}.txt"
            if label_path.exists():
                new_label_path = labels_dir / f"{new_name}.txt"
                label_path.rename(new_label_path)

def update_yaml(yaml_path, new_path):
    """
    Actualizar rutas en archivo YAML
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Actualizar rutas
    data['train'] = str(Path(new_path) / 'train' / 'images')
    data['val'] = str(Path(new_path) / 'valid' / 'images')
    data['test'] = str(Path(new_path) / 'test' / 'images')
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False)

# Rutas de los datasets originales
dataset1_path = r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\BrandLogoDetection.v6i.yolov8"
dataset2_path = r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\logo_detect_ v3.v1i.yolov8"

# Crear directorio para los nuevos datasets
output_dir = Path(r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\merged_dataset")
output_dir.mkdir(parents=True, exist_ok=True)

# Copiar y reindexar dataset 1
print("Procesando dataset 1...")
new_dataset1_path = output_dir / "brand_dataset"
copy_dataset(dataset1_path, new_dataset1_path)
reindex_dataset(new_dataset1_path, "brand")
update_yaml(new_dataset1_path / "data.yaml", new_dataset1_path)

# Copiar y reindexar dataset 2
print("Procesando dataset 2...")
new_dataset2_path = output_dir / "logo_dataset"
copy_dataset(dataset2_path, new_dataset2_path)
reindex_dataset(new_dataset2_path, "logo")
update_yaml(new_dataset2_path / "data.yaml", new_dataset2_path)

print("Proceso completado!")
print(f"Los datasets reindexados se encuentran en: {output_dir}")