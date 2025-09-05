import cv2
from model_loader import get_model
import os

def test_model_basic():
    try:
        # Cargar modelo
        model = get_model()
        print("✅ Modelo cargado correctamente")
        
        # Verificar que el archivo existe
        model_path = "models/best.pt"
        if os.path.exists(model_path):
            print(f"✅ Archivo del modelo encontrado: {model_path}")
        else:
            print(f"❌ Archivo del modelo NO encontrado: {model_path}")
            return
        
        # Información del modelo
        print(f"📊 Clases del modelo: {model.names}")
        print(f"📊 Número de clases: {len(model.names)}")
        
        # Probar con una imagen de prueba (si tienes una)
        test_image_path = "test_image.jpg"  # Cambia por una imagen real
        if os.path.exists(test_image_path):
            results = model.predict(test_image_path)
            print(f"✅ Predicción exitosa en imagen de prueba")
            
            for result in results:
                if len(result.boxes) > 0:
                    print(f"🎯 Detectados {len(result.boxes)} objetos")
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        class_name = model.names[class_id]
                        print(f"   - {class_name}: {confidence:.2f}")
                else:
                    print("❌ No se detectaron objetos")
        else:
            print(f"ℹ️ No hay imagen de prueba en {test_image_path}")
            
    except Exception as e:
        print(f"❌ Error al cargar el modelo: {e}")

if __name__ == "__main__":
    test_model_basic()