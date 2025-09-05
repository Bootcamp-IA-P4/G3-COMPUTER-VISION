from ultralytics import YOLO
import os

def test_model_from_terminal(model_path, source_path):
    """
    Carga un modelo YOLOv8 y realiza una predicción sobre una imagen, video local o URL de video.
    Muestra los resultados en la terminal.
    """
    if not os.path.exists(model_path):
        print(f"Error: El modelo no se encontró en la ruta: {model_path}")
        return

    # Comprobar si la fuente es una URL o un archivo local
    is_url = source_path.startswith('http://') or source_path.startswith('https://')

    if not is_url and not os.path.exists(source_path):
        print(f"Error: La fuente (imagen/video) no se encontró en la ruta: {source_path}")
        return

    print(f"Cargando modelo desde: {model_path}")
    model = YOLO(model_path)

    print(f"Realizando inferencia en la fuente: {source_path}")
    # Realiza la predicción. Puedes añadir 'show=True' para visualizar las detecciones en una ventana.
    # Para videos, 'save=True' guardará el video con las detecciones.
    results = model.predict(source=source_path, conf=0.25, iou=0.7, show=False, save=False)

    print("\n--- Resultados de la Inferencia ---")
    # Los resultados para videos son una lista de objetos Results, uno por cada frame
    for i, r in enumerate(results):
        if r.boxes is None or len(r.boxes) == 0:
            # print(f"Frame {i+1}: No se detectaron objetos.") # Descomentar para ver frames sin detecciones
            continue

        print(f"\nFuente: {source_path} - Frame: {i+1}" if not r.path else f"Imagen: {r.path}")
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = int(box.cls[0].item())
            class_name = model.names[cls] if hasattr(model, 'names') else f"Class {cls}"

            print(f"  - Objeto: {class_name} (ID: {cls})")
            print(f"    Confianza: {conf:.2f}")
            print(f"    Bounding Box (x1, y1, x2, y2): ({x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f})")
            print("-" * 20)

    print("\n--- Inferencia Finalizada ---")

if __name__ == '__main__':
    # --- CONFIGURACIÓN ---
    # Reemplaza estas rutas con las rutas absolutas de tu modelo y la fuente (imagen/video/URL)

    # Ejemplo de ruta de modelo (ajusta según tu caso):
    model_to_test = 'training_results/yolov8s_reduced_b4_w2_img416_80_epochs/weights/best.pt'

    # --- OPCIONES DE FUENTE ---
    # 1. Para una imagen local:
    # source_to_test = '/home/juandomingo/factoriaf5/mod03-projs/G3-COMPUTER-VISION/data/datasets/curated/dataset_v1_yolov8_reduced/test/images/some_test_image.jpg'

    # 2. Para un video local:
    # source_to_test = '/path/to/your/local/video.mp4'

    # 3. Para una URL de video (ejemplo de un video de YouTube, asegúrate de que sea accesible públicamente):
    # source_to_test = 'https://www.youtube.com/watch?v=your_video_id' # Reemplaza con una URL real

    # Placeholder paths - PLEASE UPDATE THESE!
    # Descomenta y ajusta la línea que quieras usar:
    source_to_test = 'https://www.youtube.com/watch?v=NOuQg-3VXHk&ab_channel=Coca-Cola'

    # --- EJECUCIÓN ---
    if source_to_test == 'PATH_TO_YOUR_IMAGE_OR_VIDEO_OR_URL':
        print("ADVERTENCIA: Por favor, actualiza la ruta 'source_to_test' en el script con una imagen, video o URL.")
        print("Ejemplo: python scripts/test_model.py")
    else:
        test_model_from_terminal(model_to_test, source_to_test)