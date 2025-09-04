'''
Script de Entrenamiento Documentado para YOLOv8s en CPU.

Propósito:
----------
Este script sirve como una plantilla robusta y bien documentada para entrenar
un modelo YOLOv8s (small) en un entorno local que no dispone de una GPU NVIDIA dedicada.
Está optimizado para ejecutarse en CPU, ajustando parámetros clave como el `batch_size`
y el número de `workers` para garantizar la estabilidad en máquinas con recursos limitados
(ej. 16GB de RAM, CPU de 4 núcleos).

Uso:
----
1. Asegúrate de que el dataset esté descomprimido en la ruta especificada en la sección
   de configuración.
2. Ejecuta el script desde la raíz del proyecto: 
   python3 scripts/training/train_yolov8s_local_documented.py

El script verificará la existencia del dataset, imprimirá la configuración utilizada,
entrenará el modelo y guardará todos los resultados (pesos, gráficos, etc.) en la
carpeta 'training_results'.
'''

import os
import shutil
from ultralytics import YOLO

def main():
    # =============================================================================
    # --- SECCIÓN DE CONFIGURACIÓN DETALLADA ---
    # Modifica los parámetros en esta sección según tus necesidades.
    # =============================================================================

    # --- Modelo ---
    # Se elige el modelo 'small' (s) por ser el más equilibrado para entrenar en CPU.
    # Ofrece una buena velocidad sin sacrificar demasiada precisión. El modelo 'nano' (n)
    # sería más rápido pero menos preciso; el 'medium' (m) sería demasiado lento.
    model_name = 'yolov8s.pt'

    # --- Dataset ---
    # Ruta al archivo YAML que define el dataset. Se construye la ruta de forma
    # relativa a la raíz del proyecto para que el script sea portable.
    dataset_yaml_path = os.path.join('data', 'datasets', 'curated', 'dataset_v2_yolov8_obb', 'data.yaml')

    # --- Parámetros de Entrenamiento ---
    epochs = 80  # Número de veces que el modelo verá el dataset completo.

    # --- Rutas de Salida ---
    # Carpeta principal donde se guardarán todos los resultados de los entrenamientos.
    project_folder = 'training_results'
    # Nombre específico para la carpeta de este entrenamiento. Ayuda a identificarlo.
    run_name = 'yolov8s_obb_b4_w4_img640_ep80_local_run_2'

    # --- Parámetros de Rendimiento para CPU ---
    # Es crucial ajustar estos valores para un entorno sin GPU dedicada.
    batch_size = 4       # Número de imágenes a procesar a la vez. Un valor bajo es vital para no agotar la RAM.
    workers = 4          # Hilos de CPU para la carga de datos. Un buen punto de partida es el número de núcleos de tu CPU.
                         # Si el sistema se ralentiza, prueba a bajarlo a 2.
    device = 'cpu'       # ¡IMPORTANTE! Forzamos el uso de la CPU. Evita errores si no hay GPU CUDA disponible.
    cache_images = True  # Pasa las imágenes a la RAM en la primera época para acelerar las siguientes. 
                         # Recomendado si tienes suficiente RAM (ej. >12GB).

    # --- Hiperparámetros de Optimización ---
    patience = 20        # Número de épocas sin mejora en la métrica principal antes de detener el entrenamiento (Early Stopping).
    optimizer = 'AdamW'  # Optimizador moderno que suele dar buenos resultados y una convergencia estable.
    cosine_lr = True     # Utiliza una curva de tasa de aprendizaje cosenoidal, que ayuda a ajustar el modelo de forma más fina al final.

    # =============================================================================
    # --- FIN DE LA CONFIGURACIÓN ---
    # =============================================================================

    # --- Verificación y Descarga del Modelo ---
    # Define la ruta donde se guardará el modelo y comprueba si ya existe.
    models_dir = 'models'
    model_path = os.path.join(models_dir, model_name)

    if not os.path.exists(model_path):
        print(f"El modelo '{model_name}' no se encuentra en '{models_dir}'.")
        print("Descargando modelo de Ultralytics...")
        os.makedirs(models_dir, exist_ok=True)
        
        # Al instanciar con el nombre base (ej. 'yolov8s.pt'), YOLO lo descarga
        # a un directorio de caché. Lo cargamos temporalmente para obtener la ruta
        # y luego lo movemos a nuestra carpeta de modelos deseada.
        temp_model = YOLO(model_name)
        
        # La propiedad .ckpt_path contiene la ruta al modelo descargado en la caché.
        shutil.move(temp_model.ckpt_path, model_path)
        print(f"Modelo guardado en: {model_path}")
    else:
        print(f"Modelo encontrado en: {model_path}")

    # --- Verificación de Rutas ---
    print("Verificando la ruta del dataset...")
    if not os.path.exists(dataset_yaml_path):
        # Lanza una excepción clara si no se encuentra el archivo .yaml para detener la ejecución.
        raise FileNotFoundError(
            f"[ERROR] No se encontró el archivo 'data.yaml' en la ruta: {dataset_yaml_path}"
            f"Por favor, asegúrate de que la ruta es correcta y el dataset está en su lugar."
        )
    print(f"Dataset encontrado en: {dataset_yaml_path}")

    # --- Resumen de la Configuración ---
    print("\n--- Iniht5EpOyaQ2mGDxLfS*2509ciando Entrenamiento Local en CPU ---")
    print(f"  - Modelo: '{model_name}'")
    print(f"  - Dataset: {dataset_yaml_path}")
    print(f"  - Épocas: {epochs}")
    print(f"  - Batch Size: {batch_size}")
    print(f"  - Workers: {workers}")
    print(f"  - Dispositivo: {device}")
    print(f"  - Resultados se guardarán en: {os.path.join(project_folder, run_name)}")
    print("-" * 40)

    # --- Carga y Entrenamiento del Modelo ---
    try:
        # Cargar el modelo desde la ruta local (que ya hemos verificado o descargado).
        model = YOLO(model_path)

        # Llamada al método de entrenamiento con todos los parámetros definidos.
        results = model.train(
            # Rutas y datos
            data=dataset_yaml_path,
            project=project_folder,
            name=run_name,

            # Configuración del entrenamiento
            epochs=epochs,
            imgsz=640,
            patience=patience,

            # Rendimiento y hardware
            batch=batch_size,
            workers=workers,
            device=device,
            cache=cache_images,

            # Optimizador
            optimizer=optimizer,
            cos_lr=cosine_lr,

            # Salidas y logs
            plots=True,       # Generar y guardar gráficos de métricas y resultados.
            save_json=True    # Guardar los resultados, incluidas las métricas por clase, en formato JSON.
        )

    except Exception as e:
        print(f"[ERROR] Ocurrió un error durante el entrenamiento: {e}")
        return

    # --- Finalización ---
    print("-" * 40)
    print("¡Entrenamiento finalizado con éxito!")
    results_path = os.path.join(project_folder, run_name)
    print(f"Resultados, gráficos y pesos guardados en: {results_path}")


if __name__ == '__main__':
    # Esta construcción asegura que el código dentro de este bloque solo se ejecuta
    # cuando el script es llamado directamente por el intérprete de Python.
    # Es una buena práctica estándar en scripts de Python.
    main()
