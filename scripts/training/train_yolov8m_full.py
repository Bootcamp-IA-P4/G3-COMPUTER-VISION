from ultralytics import YOLO
import os
import torch

def main():
    # --- Configuración del Entrenamiento ---
    
    # Verificar GPU
    print(f"GPU disponible: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU actual: {torch.cuda.get_device_name(0)}")
        print(f"Memoria GPU total: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
    else:
        print("¡ADVERTENCIA! No se detectó GPU. El entrenamiento será muy lento.")
        return

    # Modelo a utilizar. YOLOv8m (medium). Se descargará automáticamente si no existe.
    model_name = 'yolov8n.pt'

    # Ruta al archivo de configuración del dataset (data.yaml).
    # ¡¡ESTA ES LA LÍNEA QUE TU COMPAÑERO DEBE REVISAR Y CAMBIAR SI ES NECESARIO!!
    dataset_yaml_path = r'C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\logo_detect_v3.v1i.yolov8\data.yaml'

    # Parámetros de entrenamiento
    epochs = 50
    project_folder = 'training_results'
    run_name = 'yolov8n_full_dataset_50_epochs_py'

    # --- Fin de la Configuración ---

    print(f"Iniciando el entrenamiento del modelo '{model_name}'...")
    print(f"Dataset: {dataset_yaml_path}")
    print(f"Epochs: {epochs}")

    # Cargar el modelo
    model = YOLO(model_name)

    # Entrenar el modelo (parámetros optimizados para CPU)
    results = model.train(
        data=dataset_yaml_path,
        epochs=epochs,
        project=project_folder,
        name=run_name,
        save_json=True,
        plots=True,
        batch=4,           # Batch pequeño para evitar sobrecarga de RAM
        workers=2,         # Menos workers para evitar saturar CPU
        device='cpu',      # Forzar uso de CPU
        cache=False,       # Desactivar cache para evitar uso excesivo de RAM
        amp=False,         # Mixed precision no disponible en CPU
        imgsz=416,         # Reducir tamaño de imagen para acelerar procesamiento
        optimizer='Adam',  # Adam suele converger más rápido en CPU
        rect=True,         # Rectangular training para eficiencia
        mosaic=0.0,        # Desactivar mosaic para acelerar
        close_mosaic=0,    # No usar mosaic al final
        multi_scale=False, # Desactivar multi-escala para acelerar
        lr0=0.01,          # Learning rate inicial
        lrf=0.01,          # Learning rate final
        momentum=0.937,    # Momentum para Adam
        weight_decay=0.0005, # Regularización L2
        warmup_epochs=2,   # Menos warmup para CPU
        warmup_momentum=0.8,
        warmup_bias_lr=0.1,
        box=7.5,
        cls=0.5,
        dfl=1.5,
        verbose=True,
        seed=0,
        deterministic=True
    )

    print("-" * 30)
    print(f"Entrenamiento finalizado.")
    results_path = os.path.join(project_folder, run_name)
    print(f"Resultados guardados en: {results_path}")

    # Liberar memoria GPU
    torch.cuda.empty_cache()

if __name__ == '__main__':
    main()
