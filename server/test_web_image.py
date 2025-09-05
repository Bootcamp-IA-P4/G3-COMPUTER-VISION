import requests
from PIL import Image
from model_loader import get_model
import numpy as np

def test_model_web_image():
    try:
        model = get_model()
        
        # Descargar una imagen de prueba de internet
        url = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"
        response = requests.get(url)
        
        if response.status_code == 200:
            with open("temp_test.jpg", "wb") as f:
                f.write(response.content)
            
            print("✅ Imagen descargada")
            
            # Predecir
            results = model.predict("temp_test.jpg")
            
            for result in results:
                print(f"🎯 Detectados {len(result.boxes)} objetos")
                for box in result.boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    class_name = model.names[class_id]
                    print(f"   - {class_name}: {confidence:.2f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_model_web_image()