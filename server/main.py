from fastapi import FastAPI, HTTPException
from database.connection import get_supabase
from database.schemas import BrandCreate, BrandUpdate, Brand
from database.schemas import Video, VideoCreate, VideoUpdate
from database.schemas import Detection, DetectionCreate, DetectionUpdate
from model_loader import get_model
import hashlib
import os
import cv2
import yt_dlp

app = FastAPI(title="Logo Detection Backend")

# Conexión global a Supabase
supabase = get_supabase()

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"status": "ok", "service": "logo-detection-backend"}

# ------------------------------
# CRUD Brands
# ------------------------------
@app.post("/brands/", response_model=Brand)
def create_brand(brand: BrandCreate):
    existing = supabase.table("brands").select("*").eq("name", brand.name).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Brand already exists")
    res = supabase.table("brands").insert({"name": brand.name}).execute()
    return res.data[0]

@app.get("/brands/", response_model=list[Brand])
def list_brands():
    res = supabase.table("brands").select("*").execute()
    return res.data

@app.put("/brands/{brand_id}", response_model=Brand)
def update_brand(brand_id: int, brand: BrandUpdate):
    res = supabase.table("brands").update({"name": brand.name}).eq("id", brand_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return res.data[0]

@app.delete("/brands/{brand_id}")
def delete_brand(brand_id: int):
    res = supabase.table("brands").delete().eq("id", brand_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Brand not found")
    return {"detail": "Brand deleted"}

# ------------------------------
# CRUD Videos
# ------------------------------
@app.post("/videos/", response_model=Video)
def create_video(video: VideoCreate):
    res = supabase.table("videos").insert({
        "filename": video.filename,
        "path": video.path,
        "duration": video.duration
    }).execute()
    return res.data[0]

@app.get("/videos/", response_model=list[Video])
def list_videos():
    res = supabase.table("videos").select("*").execute()
    return res.data

@app.get("/videos/{video_id}", response_model=Video)
def get_video(video_id: int):
    res = supabase.table("videos").select("*").eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return res.data[0]

@app.put("/videos/{video_id}", response_model=Video)
def update_video(video_id: int, video: VideoUpdate):
    update_data = {k: v for k, v in video.dict().items() if v is not None}
    res = supabase.table("videos").update(update_data).eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return res.data[0]

@app.delete("/videos/{video_id}")
def delete_video(video_id: int):
    res = supabase.table("videos").delete().eq("id", video_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"detail": "Video deleted"}

# ------------------------------
# CRUD Detections
# ------------------------------
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

@app.get("/detections/", response_model=list[Detection])
def list_detections():
    res = supabase.table("detections").select("*").execute()
    return res.data

@app.get("/detections/{detection_id}", response_model=Detection)
def get_detection(detection_id: int):
    res = supabase.table("detections").select("*").eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return res.data[0]

@app.put("/detections/{detection_id}", response_model=Detection)
def update_detection(detection_id: int, detection: DetectionUpdate):
    update_data = {k: v for k, v in detection.dict().items() if v is not None}
    res = supabase.table("detections").update(update_data).eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return res.data[0]

@app.delete("/detections/{detection_id}")
def delete_detection(detection_id: int):
    res = supabase.table("detections").delete().eq("id", detection_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Detection not found")
    return {"detail": "Detection deleted"}

# ------------------------------
# Procesar Video desde URL con yt-dlp
# ------------------------------
@app.post("/process-video-url/")
def process_video_url(video_url: str):
    """
    Descargar video de YouTube con yt-dlp, guardarlo en uploads/ y procesarlo con YOLO.
    """
    # Generar nombre único
    url_hash = hashlib.md5(video_url.encode()).hexdigest()
    filename = f"{url_hash}.mp4"
    local_path = os.path.join(UPLOADS_DIR, filename)

    # Descargar video con yt-dlp
    try:
        ydl_opts = {
            'outtmpl': local_path,
            'format': 'mp4',
            'quiet': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"No se pudo descargar el video: {e}")

    # Guardar metadatos en BD
    video_res = supabase.table("videos").insert({
        "filename": filename,
        "path": local_path,
        "url": video_url
    }).execute()
    video_id = video_res.data[0]["id"]

    # Cargar modelo YOLO
    try:
        model = get_model()
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Abrir video y procesar frames
    cap = cv2.VideoCapture(local_path)
    if not cap.isOpened():
        raise HTTPException(status_code=500, detail="No se pudo abrir el video")

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        results = model.predict(frame)
        for res in results:
            for box in res.boxes:
                det_data = {
                    "video_id": video_id,
                    "brand_id": None,
                    "start_time": frame_idx / cap.get(cv2.CAP_PROP_FPS),
                    "end_time": frame_idx / cap.get(cv2.CAP_PROP_FPS),
                    "confidence": float(box.conf[0]),
                    "bbox_image_path": None
                }
                supabase.table("detections").insert(det_data).execute()

    cap.release()

    return {
        "status": "processing_finished",
        "video_id": video_id,
        "filename": filename,
        "frames_processed": frame_idx
    }

