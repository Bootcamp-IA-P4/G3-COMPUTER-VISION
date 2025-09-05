from pydantic import BaseModel, HttpUrl
from typing import Optional

# -------------------------------
# Esquemas de Brands
# -------------------------------
class BrandCreate(BaseModel):
    name: str

class BrandUpdate(BaseModel):
    name: Optional[str]

class Brand(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

# -------------------------------
# Esquemas de Videos
# -------------------------------
class VideoCreate(BaseModel):
    filename: str
    path: Optional[str] = None  # Para ruta local si se descarga
    url: Optional[HttpUrl] = None  # Nueva opción: URL del video
    duration: Optional[float] = None  # en segundos

class VideoUpdate(BaseModel):
    filename: Optional[str] = None
    path: Optional[str] = None
    url: Optional[HttpUrl] = None
    duration: Optional[float] = None

class Video(BaseModel):
    id: int
    filename: str
    path: Optional[str]
    url: Optional[HttpUrl] = None
    uploaded_at: Optional[str]
    duration: Optional[float]

    class Config:
        from_attributes = True

# -------------------------------
# Esquemas de Detections
# -------------------------------
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
        from_attributes = True
