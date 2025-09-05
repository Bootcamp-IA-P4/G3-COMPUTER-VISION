from database.connection import get_supabase

def fix_null_brand_ids():
    supabase = get_supabase()
    
    # Eliminar registros con brand_id NULL
    result = supabase.table("detections").delete().is_("brand_id", "null").execute()
    
    print(f"Eliminados {len(result.data)} registros con brand_id NULL")

if __name__ == "__main__":
    fix_null_brand_ids()