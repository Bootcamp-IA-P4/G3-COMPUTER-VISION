from ultralytics import YOLO
import os

def main():
    # --- Configuración del Entrenamiento ---

    # Modelo a utilizar. YOLOv8m (medium). Se descargará automáticamente si no existe.
    model_name = 'yolov8m.pt'

    # Ruta relativa al archivo de configuración del dataset (data.yaml) desde la raíz del proyecto.
    dataset_yaml_path = 'data/datasets/curated/dataset_v1_yolov8/data.yaml'

    # Parámetros de entrenamiento
    epochs = 80
    project_folder = 'training_results'
    run_name = 'yolov8m_full_b8_w4_img640_80_epochs' # Actualizado para reflejar nuevos params

    # Parámetros de rendimiento para sobremesa
    batch_size = 8
    workers = 4
    image_size = 640

    # --- Fin de la Configuración ---

    print(f"Iniciando el entrenamiento del modelo '{model_name}'...")
    print(f"Dataset: {dataset_yaml_path}")
    print(f"Epochs: {epochs}")
    print(f"Params: batch={batch_size}, workers={workers}, imgsz={image_size}")

    # Cargar el modelo
    model = YOLO(model_name)

    # Entrenar el modelo
    results = model.train(
        data=dataset_yaml_path,
        epochs=epochs,
        project=project_folder,
        name=run_name,
        batch=batch_size,
        workers=workers,
        imgsz=image_size,
        save_json=True,
        save_hybrid=True,
        plots=True
    )

    print("-" * 30)
    print(f"Entrenamiento finalizado.")
    results_path = os.path.join(project_folder, run_name)
    print(f"Resultados guardados en: {results_path}")

if __name__ == '__main__':
    main()
