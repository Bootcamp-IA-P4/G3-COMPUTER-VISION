""" 
Script de Entrenamiento Documentado para YOLOv8s en CPU (Run 2).

Configuración:
- epochs: 80
- imgsz: 640
- batch: 4
- workers: 2 (ajustado para CPU)

Nota: El entrenamiento en CPU es inherentemente lento. Este script está optimizado
para la estabilidad, no para la velocidad. """

import os
import shutil
from ultralytics import YOLO

def main():
    # =============================================================================
    # --- SECCIÓN DE CONFIGURACIÓN DETALLADA ---
    # =============================================================================

    # --- Modelo ---
    model_name = 'yolov8s.pt'

    # --- Dataset ---
    dataset_yaml_path = os.path.join('data', 'datasets', 'curated', 'dataset_v2_yolov8_obb', 'data.yaml')

    # --- Parámetros de Entrenamiento ---
    epochs = 80
    img_size = 640

    # --- Rutas de Salida ---
    project_folder = 'training_results'
    run_name = 'yolov8s_obb_b4_w2_img640_ep80_local_run_2'

    # --- Parámetros de Rendimiento para CPU ---
    batch_size = 4
    workers = 2  # Reducido a 2 para evitar sobrecargar la CPU.
    device = 'cpu'
    cache_images = True

    # --- Hiperparámetros de Optimización ---
    patience = 20
    optimizer = 'AdamW'
    cosine_lr = True

    # =============================================================================
    # --- FIN DE LA CONFIGURACIÓN ---
    # =============================================================================

    # --- Verificación y Descarga del Modelo ---
    models_dir = 'models'
    model_path = os.path.join(models_dir, model_name)

    if not os.path.exists(model_path):
        print(f"El modelo '{model_name}' no se encuentra en '{models_dir}'.")
        print("Descargando modelo de Ultralytics...")
        os.makedirs(models_dir, exist_ok=True)
        temp_model = YOLO(model_name)
        shutil.move(temp_model.ckpt_path, model_path)
        print(f"Modelo guardado en: {model_path}")
    else:
        print(f"Modelo encontrado en: {model_path}")

    # --- Verificación de Rutas ---
    if not os.path.exists(dataset_yaml_path):
        raise FileNotFoundError(f"[ERROR] No se encontró el archivo 'data.yaml' en: {dataset_yaml_path}")
    print(f"Dataset encontrado en: {dataset_yaml_path}")

    # --- Carga y Entrenamiento del Modelo ---
    print("\n--- Iniciando Entrenamiento Local en CPU ---")
    model = YOLO(model_path)

    results = model.train(
        data=dataset_yaml_path,
        project=project_folder,
        name=run_name,
        epochs=epochs,
        patience=patience,
        batch=batch_size,
        imgsz=img_size,
        workers=workers,
        device=device,
        cache=cache_images,
        optimizer=optimizer,
        cos_lr=cosine_lr,
        plots=True,
        save_json=True
    )

    print("--- ENTRENAMIENTO FINALIZADO ---")
    print(f"Resultados guardados en: {results.save_dir}")

if __name__ == '__main__':
    main()
