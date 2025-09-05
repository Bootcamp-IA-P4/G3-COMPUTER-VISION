from ultralytics import YOLO
import os

def main():
    # --- Configuración del Entrenamiento ---

    # Modelo a utilizar. YOLOv8m (medium). Se descargará automáticamente si no existe.
    model_name = 'yolov8m.pt'

    # Ruta al archivo de configuración del dataset (data.yaml).
    # dataset_yaml_path = '/home/juandomingo/factoriaf5/mod03-projs/G3-COMPUTER-VISION/data/datasets/curated/dataset_v1_yolov8m_reduced/data.yaml'
    # Ruta relativa al archivo de configuración del dataset (data.yaml) desde la raíz del proyecto.
    dataset_yaml_path = 'data/datasets/curated/dataset_v1_yolov8_reduced/data.yaml'

    # Parámetros de entrenamiento
    epochs = 80
    project_folder = 'training_results'
    run_name = 'yolov8m_reduced_b8_w4_img640_80_epochs' # Nombre actualizado para reflejar los nuevos parámetros

    # --- Fin de la Configuración ---

    # --- Verificación del Dataset ---
    if not os.path.exists(dataset_yaml_path):
        print(f"ERROR: El archivo data.yaml no se encontró en {dataset_yaml_path}.")
        print("Asegúrate de que la ruta sea correcta y el archivo exista.")
        return # Salir si el dataset no se encuentra

    print(f"Iniciando el entrenamiento del modelo '{model_name}' con el DATASET REDUCIDO...")
    print(f"Dataset: {dataset_yaml_path}")
    print(f"Epochs: {epochs}")

    # Cargar el modelo
    model = YOLO(model_name)

    # Entrenar el modelo
    results = model.train(
        data=dataset_yaml_path,
        epochs=epochs,
        project=project_folder,
        name=run_name,
        save_json=True,
        save_hybrid=True,
        plots=True,
        # --- Parámetros de rendimiento y optimización ---
        batch=8,
        workers=4,
        imgsz=640,
        patience=20, # Early stopping: detiene el entrenamiento si no hay mejora en 20 épocas
        cache=True,  # Cachea las imágenes en RAM para acelerar la carga (si la RAM lo permite)
        optimizer='AdamW', # Optimizador AdamW para una convergencia más estable
        cos_lr=True, # Usa decaimiento de learning rate con coseno annealing
    )

    print("-" * 30)
    print(f"Entrenamiento finalizado.")
    results_path = os.path.join(project_folder, run_name)
    print(f"Resultados guardados en: {results_path}")

if __name__ == '__main__':
    main()
