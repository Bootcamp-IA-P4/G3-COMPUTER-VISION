"""
Script de Entrenamiento Documentado y Avanzado para YOLOv8s en CPU.

Propósito:
----------
Este script entrena un modelo YOLOv8s en un entorno de CPU, con una configuración
optimizada para obtener un resultado en un tiempo razonable. Incluye parámetros
avanzados para control de aumentación, optimizador y reproducibilidad, con cada
opción comentada para facilitar su comprensión y modificación.

Implementa una lógica de reanudación automática desde checkpoints.

Configuración de Sacrificio:
- epochs: 25
- imgsz: 320
- batch: 4
- workers: 2
"""

import os
import shutil
from ultralytics import YOLO

def main():
    # =============================================================================
    # --- SECCIÓN DE CONFIGURACIÓN DETALLADA ---
    # =============================================================================

    # --- Modelo ---
    model_name = 'yolov8s.pt'
    models_dir = 'models'
    base_model_path = os.path.join(models_dir, model_name)

    # --- Dataset ---
    dataset_yaml_path = os.path.join('data', 'datasets', 'curated', 'dataset_v2_yolov8_obb', 'data.yaml')

    # --- Parámetros de Entrenamiento ---
    epochs = 25
    img_size = 320

    # --- Rutas de Salida ---
    project_folder = 'training_results'
    run_name = 'yolov8s_obb_fast_local_run_documented'

    # --- Parámetros de Rendimiento para CPU ---
    batch_size = 4
    workers = 2
    device = 'cpu'
    cache_images = True

    # --- Hiperparámetros de Optimización ---
    patience = 50  # Aumentada la paciencia para Early Stopping
    optimizer = 'AdamW'

    # =============================================================================
    # --- LÓGICA DE REANUDACIÓN Y CARGA DE MODELO ---
    # =============================================================================

    model_to_load = base_model_path

    last_checkpoint_path = os.path.join(project_folder, run_name, 'weights', 'last.pt')

    if os.path.exists(last_checkpoint_path):
        print(f"Checkpoint encontrado en: {last_checkpoint_path}")
        print("Se reanudará el entrenamiento desde este punto.")
        model_to_load = last_checkpoint_path
    else:
        print("No se encontró checkpoint. Empezando un nuevo entrenamiento.")
        if not os.path.exists(base_model_path):
            print(f"El modelo base '{model_name}' no se encuentra. Descargando...")
            os.makedirs(models_dir, exist_ok=True)
            temp_model = YOLO(model_name)
            shutil.move(temp_model.ckpt_path, base_model_path)
            print(f"Modelo guardado en: {base_model_path}")

    if not os.path.exists(dataset_yaml_path):
        raise FileNotFoundError(f"[ERROR] No se encontró el archivo 'data.yaml' en: {dataset_yaml_path}")
    print(f"Dataset encontrado en: {dataset_yaml_path}")

    print(f"\n--- Cargando modelo: {model_to_load} ---")
    model = YOLO(model_to_load)

    # =============================================================================
    # --- LLAMADA AL ENTRENAMIENTO ---
    # =============================================================================
    results = model.train(
        # --- Configuración Principal ---
        data=dataset_yaml_path,         # Ruta al archivo data.yaml.
        project=project_folder,         # Carpeta raíz para guardar los resultados.
        name=run_name,                  # Nombre de la carpeta específica para este run.
        epochs=epochs,                  # Número de épocas a entrenar.
        patience=patience,              # Épocas a esperar por si no hay mejora antes de parar (Early Stopping).
        
        # --- Rendimiento y Hardware ---
        batch=batch_size,               # Tamaño del lote.
        imgsz=img_size,                 # Tamaño de la imagen de entrada.
        workers=workers,                # Hilos de la CPU para cargar datos.
        device=device,                  # Dispositivo a usar ('cpu' o '0' para GPU).
        cache=cache_images,             # Cachear imágenes en RAM para acelerar la carga.
        amp=False,                      # Automatic Mixed Precision. Poner a False en CPU, solo para GPUs NVIDIA.

        # --- Checkpoints y Validación ---
        save=True,                      # Guardar checkpoints y resultados finales (siempre True por defecto).
        save_period=10,                 # Guardar un checkpoint del modelo cada 10 épocas.
        val=True,                       # Realizar validación al final de cada época.

        # --- Aumentación de Datos y Regularización ---
        # NOTA: La aumentación consume CPU. Para un entrenamiento más rápido, se pueden reducir estos valores.
        mosaic=1.0,                     # Probabilidad de usar aumentación de mosaico.
        degrees=0.0,                    # Rango de rotación de la imagen (+/- grados).
        translate=0.1,                  # Rango de traslación de la imagen (+/- fracción).
        scale=0.5,                      # Rango de escalado de la imagen (+/- ganancia).
        shear=0.0,                      # Rango de distorsión de la imagen (+/- grados).
        perspective=0.0,                # Rango de distorsión de perspectiva.
        flipud=0.0,                     # Probabilidad de volteo vertical (arriba-abajo).
        fliplr=0.5,                     # Probabilidad de volteo horizontal (izquierda-derecha).
        multi_scale=True,               # Variar el tamaño de la imagen entre +/- 50% de imgsz.

        # --- Hiperparámetros del Optimizador ---
        optimizer=optimizer,            # Optimizador a usar (ej. 'AdamW', 'SGD').
        lr0=0.01,                       # Tasa de aprendizaje inicial.
        lrf=0.01,                       # Tasa de aprendizaje final = lr0 * lrf.
        momentum=0.937,                 # Momento del optimizador SGD.
        weight_decay=0.0005,            # Regularización por decaimiento de peso.
        
        # --- Salidas y Logs ---
        plots=True,                     # Guardar gráficos de métricas y curvas al finalizar.
        save_json=True,                 # Guardar las métricas en un archivo JSON.
        verbose=True,                   # Imprimir información detallada durante el entrenamiento.
        
        # --- Reproducibilidad ---
        seed=42,                        # Semilla aleatoria para resultados reproducibles.
        deterministic=True              # Forzar algoritmos deterministas, ayuda a la reproducibilidad.
    )

    print("--- ENTRENAMIENTO FINALIZADO ---")
    print(f"Resultados guardados en: {results.save_dir}")

if __name__ == '__main__':
    main()