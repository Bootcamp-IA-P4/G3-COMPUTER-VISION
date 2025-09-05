# G3-COMPUTER-VISION
# Brand Detection System

Sistema de detección de marcas en videos utilizando inteligencia artificial con YOLO y Computer Vision.

## Descripción del Proyecto

Este proyecto implementa un sistema completo de detección de logos en videos para empresas de publicidad que necesitan medir el tiempo de exposición de marcas en contenido audiovisual. El sistema utiliza un modelo YOLO entrenado para detectar logos específicos (Adidas, Coca-Cola, y logos genéricos) en videos de YouTube y otras plataformas.

## Características Principales

- **Detección automática de logos** en videos usando YOLO
- **Procesamiento de videos** desde URLs de YouTube/Vimeo con yt-dlp
- **Interface web moderna** con Streamlit y diseño profesional
- **API REST** con FastAPI para integración
- **Base de datos** Supabase para almacenamiento persistente
- **Visualizaciones interactivas** con Plotly
- **Almacenamiento de crops** en Supabase Storage

## Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   Streamlit     │◄──►│    FastAPI      │◄──►│   Supabase      │
│                 │    │                 │    │                 │
│ - Dashboard     │    │ - Video Proc.   │    │ - Videos        │
│ - Process Video │    │ - YOLO Model    │    │ - Brands        │
│ - Analytics     │    │ - API Endpoints │    │ - Detections    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web para API REST
- **YOLO (Ultralytics)** - Modelo de detección de objetos
- **OpenCV** - Procesamiento de imágenes
- **yt-dlp** - Descarga de videos
- **Supabase** - Base de datos y almacenamiento

### Frontend
- **Streamlit** - Framework para aplicaciones web
- **Plotly** - Visualizaciones interactivas
- **Pandas** - Manipulación de datos
- **CSS personalizado** - Diseño profesional

### Modelo de IA
- **YOLO v8** - Detección de objetos en tiempo real
- **Clases detectadas**: Adidas Logo, Coca-Cola, Logo genérico

## Estructura del Proyecto

```
G3-COMPUTER-VISION/
├── server/                     # Backend FastAPI
│   ├── main.py                # Aplicación principal
│   ├── model_loader.py        # Cargador del modelo YOLO
│   ├── database/              # Configuración de BD
│   │   ├── connection.py      # Conexión Supabase
│   │   └── schemas.py         # Esquemas Pydantic
│   ├── models/                # Modelos entrenados
│   │   └── best.pt           # Modelo YOLO entrenado
│   └── uploads/              # Archivos temporales
├── frontend_streamlit.py      # Frontend Streamlit
├── logo.png                   # Logo del proyecto (opcional)
├── requirements.txt           # Dependencias
└── README.md                 # Este archivo
```

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip
- Cuenta de Supabase

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd G3-COMPUTER-VISION
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Supabase
1. Crea un proyecto en [Supabase](https://supabase.com)
2. Configura las credenciales en `server/database/connection.py`
3. Crea las siguientes tablas:

```sql
-- Tabla de marcas
CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Tabla de videos
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    path VARCHAR(500),
    url VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT NOW(),
    duration FLOAT
);

-- Tabla de detecciones
CREATE TABLE detections (
    id SERIAL PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id),
    brand_id INTEGER REFERENCES brands(id),
    start_time FLOAT NOT NULL,
    end_time FLOAT NOT NULL,
    confidence FLOAT,
    bbox_image_path VARCHAR(500)
);
```

### 5. Configurar Storage Buckets
Crea los siguientes buckets en Supabase Storage:
- `videos` - Para almacenar videos procesados
- `crops` - Para almacenar recortes de detecciones

## Uso del Sistema

### 1. Iniciar el Backend
```bash
cd server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Iniciar el Frontend
```bash
streamlit run frontend_streamlit.py
```

### 3. Acceder a la Aplicación
- **Frontend**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Funcionalidades

### Dashboard
- Métricas en tiempo real de videos procesados
- Gráficos de marcas más detectadas
- Distribución de niveles de confianza
- Videos procesados recientemente

### Procesamiento de Videos
- Entrada de URLs de YouTube/Vimeo
- Barra de progreso en tiempo real
- Detección automática de logos
- Almacenamiento de resultados

### Gestión de Videos
- Lista de todos los videos procesados
- Filtros por nombre y número de detecciones
- Estadísticas por video
- Enlaces a videos originales

### Gestión de Marcas
- Tabla interactiva de marcas detectadas
- Gráficos de rendimiento por marca
- Estadísticas de confianza promedio

## API Endpoints

### Videos
- `GET /videos/` - Listar todos los videos
- `POST /videos/` - Crear nuevo video
- `GET /videos/{id}` - Obtener video específico
- `PUT /videos/{id}` - Actualizar video
- `DELETE /videos/{id}` - Eliminar video

### Marcas
- `GET /brands/` - Listar todas las marcas
- `POST /brands/` - Crear nueva marca
- `PUT /brands/{id}` - Actualizar marca
- `DELETE /brands/{id}` - Eliminar marca

### Detecciones
- `GET /detections/` - Listar todas las detecciones
- `POST /detections/` - Crear nueva detección
- `GET /detections/{id}` - Obtener detección específica
- `PUT /detections/{id}` - Actualizar detección
- `DELETE /detections/{id}` - Eliminar detección

### Procesamiento
- `POST /process-video-url/` - Procesar video desde URL

## Resultados de Pruebas

En pruebas realizadas con videos de YouTube:
- **Videos procesados**: 1
- **Frames analizados**: 360
- **Logos detectados**: 4 instancias
  - Coca-Cola: 3 detecciones
  - Adidas Logo: 1 detección
- **Confianza promedio**: >80%

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## Contacto

- **Proyecto**: Brand Detection System
- **Tecnología**: Computer Vision + IA
- **Framework**: FastAPI + Streamlit

## Reconocimientos

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) - Modelo de detección
- [Streamlit](https://streamlit.io/) - Framework de frontend
- [FastAPI](https://fastapi.tiangolo.com/) - Framework de backend
- [Supabase](https://supabase.com/) - Base de datos y almacenamiento
