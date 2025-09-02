from ultralytics import YOLO
import os

def main():
    # --- Configuración del Entrenamiento ---

    # Modelo a utilizar. YOLOv8s (small).
    model_name = 'yolov8s.pt'

    # Ruta al archivo de configuración del dataset (data.yaml).
    #dataset_yaml_path = '/home/juandomingo/factoriaf5/mod03-projs/G3-COMPUTER-VISION/data/datasets/curated/dataset_v1_yolov8m_reduced/data.yaml'
    # Ruta relativa al archivo de configuración del dataset (data.yaml) desde la raíz del proyecto.                    │
    dataset_yaml_path = 'data/datasets/curated/dataset_v1_yolov8m/data.yaml'   

    # Parámetros de entrenamiento
    epochs = 80
    project_folder = 'training_results'
    run_name = 'yolov8s_reduced_b4_w2_img416_80_epochs'

    # --- Fin de la Configuración ---

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
        # --- Optimizaciones para reducir consumo de memoria ---
        batch=4,
        workers=2,
        imgsz=416
    )

    print("-" * 30)
    print(f"Entrenamiento finalizado.")
    results_path = os.path.join(project_folder, run_name)
    print(f"Resultados guardados en: {results_path}")

if __name__ == '__main__':
    main()
