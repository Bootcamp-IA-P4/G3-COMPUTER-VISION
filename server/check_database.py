from database.connection import get_supabase

def check_detections():
    supabase = get_supabase()
    
    # Ver todas las detecciones
    result = supabase.table("detections").select("*").execute()
    
    print(f"Total detecciones: {len(result.data)}")
    
    for i, detection in enumerate(result.data):
        print(f"Detección {i+1}: ID={detection.get('id')}, brand_id={detection.get('brand_id')}, video_id={detection.get('video_id')}")
        
        # Revisar si brand_id es None, vacío, o string "null"
        if detection.get('brand_id') is None:
            print(f"  ⚠️ Esta detección tiene brand_id = None")
        elif detection.get('brand_id') == "null":
            print(f"  ⚠️ Esta detección tiene brand_id = 'null' (string)")
        elif str(detection.get('brand_id')).strip() == "":
            print(f"  ⚠️ Esta detección tiene brand_id vacío")

if __name__ == "__main__":
    check_detections()