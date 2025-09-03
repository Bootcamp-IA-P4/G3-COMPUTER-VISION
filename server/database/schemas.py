from pydantic import BaseModel
from typing import Optional

# Para crear o actualizar marcas
class BrandCreate(BaseModel):
    name: str

class BrandUpdate(BaseModel):
    name: Optional[str]

# Para devolver marcas desde la base de datos
class Brand(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# ---- Esquemas de Videos ----

class VideoCreate(BaseModel):
    filename: str
    path: Optional[str] = None
    duration: Optional[float] = None  # en segundos

class VideoUpdate(BaseModel):
    filename: Optional[str] = None
    path: Optional[str] = None
    duration: Optional[float] = None

class Video(BaseModel):
    id: int
    filename: str
    path: Optional[str]
    uploaded_at: Optional[str]
    duration: Optional[float]

    class Config:
        orm_mode = True

# ---- Esquemas de Detections ----

class DetectionCreate(BaseModel):
    video_id: int
    brand_id: int
    start_time: float
    end_time: float
    confidence: Optional[float] = None
    bbox_image_path: Optional[str] = None

class DetectionUpdate(BaseModel):
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    confidence: Optional[float] = None
    bbox_image_path: Optional[str] = None

class Detection(BaseModel):
    id: int
    video_id: int
    brand_id: int
    start_time: float
    end_time: float
    confidence: Optional[float]
    bbox_image_path: Optional[str]

    class Config:
        orm_mode = True