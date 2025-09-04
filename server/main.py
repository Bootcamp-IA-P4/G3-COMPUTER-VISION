from fastapi import FastAPI
from database.connection import get_supabase
from fastapi import HTTPException
from database.schemas import BrandCreate, BrandUpdate, Brand
from database.schemas import Video, VideoCreate, VideoUpdate
from database.schemas import Detection, DetectionCreate, DetectionUpdate

app = FastAPI(title="Logo Detection Backend")

# Conexión global a Supabase
supabase = get_supabase()

@app.get("/")
def root():
    return {"status": "ok", "service": "logo-detection-backend"}

@app.get("/test-db")
def test_db():
    """
    Probar lectura de la tabla 'videos'
    """
    supabase = get_supabase()
    try:
        res = supabase.table("videos").select("*").limit(5).execute()
        return {"videos": res.data}
    except Exception as e:
        return {"error": str(e)}

# --------- CRUD Brands ---------

# Crear nueva marca
@app.post("/brands/", response_model=Brand)
def create_brand(brand: BrandCreate):
    # Verificar si ya existe
    existing = supabase.table("brands").select("*").eq("name", brand.name).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Brand already exists")
    
    res = supabase.table("brands").insert({"name": brand.name}).execute()
    return res.data[0]

# Listar todas las marcas
@app.get("/brands/", response_model=list[Brand])
def list_brands():
    res = supabase.table("brands").select("*").execute()
    return res.data

# Actualizar marca por id
@app.put("/brands/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, brand: BrandUpdate):
    res = supabase.table("brands").update({"name": brand.name}).eq("id", brand_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return res.data[0]

# Borrar marca por id
@app.delete("/brands/{brand_id}")
def delete_brand(brand_id: int):
    res = supabase.table("brands").delete().eq("id", brand_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"detail": "Brand deleted"}

# --------- CRUD Videos ---------

# Crear nuevo vídeo
@app.post("/videos/", response_model=Video)
def create_video(video: VideoCreate):
    res = supabase.table("videos").insert({
        "filename": video.filename,
        "path": video.path,
        "duration": video.duration
    }).execute()
    return res.data[0]

# Listar todos los vídeos
@app.get("/videos/", response_model=list[Video])
def list_videos():
    res = supabase.table("videos").select("*").execute()
    return res.data

# Obtener un vídeo por id
@app.get("/videos/{video_id}", response_model=Video)
def get_video(video_id: int):
    res = supabase.table("videos").select("*").eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return res.data[0]

# Actualizar vídeo por id
@app.put("/videos/{video_id}", response_model=Video)
def update_video(video_id: int, video: VideoUpdate):
    update_data = {k: v for k, v in video.dict().items() if v is not None}
    res = supabase.table("videos").update(update_data).eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return res.data[0]

# Borrar vídeo por id
@app.delete("/videos/{video_id}")
def delete_video(video_id: int):
    res = supabase.table("videos").delete().eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"detail": "Video deleted"}


# --------- CRUD Detections ---------

# Crear nueva detección
@app.post("/detections/", response_model=Detection)
def create_detection(detection: DetectionCreate):
    res = supabase.table("detections").insert({
        "video_id": detection.video_id,
        "brand_id": detection.brand_id,
        "start_time": detection.start_time,
        "end_time": detection.end_time,
        "confidence": detection.confidence,
        "bbox_image_path": detection.bbox_image_path
    }).execute()
    return res.data[0]

# Listar todas las detecciones
@app.get("/detections/", response_model=list[Detection])
def list_detections():
    res = supabase.table("detections").select("*").execute()
    return res.data

# Obtener una detección por id
@app.get("/detections/{detection_id}", response_model=Detection)
def get_detection(detection_id: int):
    res = supabase.table("detections").select("*").eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return res.data[0]

# Actualizar detección por id
@app.put("/detections/{detection_id}", response_model=Detection)
def update_detection(detection_id: int, detection: DetectionUpdate):
    update_data = {k: v for k, v in detection.dict().items() if v is not None}
    res = supabase.table("detections").update(update_data).eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return res.data[0]

# Borrar detección por id
@app.delete("/detections/{detection_id}")
def delete_detection(detection_id: int):
    res = supabase.table("detections").delete().eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return {"detail": "Detection deleted"}

# -------------------------------
# Procesar Video (con el modelo)
# -------------------------------
@app.post("/process-video/{video_id}")
def process_video(video_id: int):
    """
    Procesar un video y generar detecciones usando el modelo entrenado.
    """
    # 1. Obtener metadatos del video desde la BD
    video_res = supabase.table("videos").select("*").eq("id", video_id).execute()
    if not video_res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    video = video_res.data[0]

    # 2. Aquí se cargaría el modelo entrenado
    # Ejemplo:
    # import pickle
    # with open("ruta_al_modelo.pkl", "rb") as f:
    #     model = pickle.load(f)

    # 3. Aquí iría la lógica de detección en frames del video
    # detections = model.detect(video["path"])
    # for det in detections:
    #     supabase.table("detections").insert({...}).execute()

    return {
        "status": "processing_started",
        "video_id": video_id,
        "filename": video["filename"]
    }