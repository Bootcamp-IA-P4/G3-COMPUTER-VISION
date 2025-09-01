import streamlit as st
import json
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
import time
from api_client import BrandDetectionAPI, validate_video_file, format_file_size

# Configuración de la página
st.set_page_config(
    page_title="Brand Detection System",
    page_icon="🎯",
    layout="wide"
)

# ==================== ESTILOS GLOBALES ====================
def apply_spotly_theme():
    st.markdown("""
        <style>
        /* Colores principales basados en Spotly */
        :root {
            --primary-purple: #5B4BDE;
            --secondary-purple: #4A3BC7;
            --dark-purple: #382F93;
            --accent-purple: #6D5FE8;
            --light-purple: rgba(91, 75, 222, 0.1);
        }
        
        /* Fondo principal de la app */
        .stApp {
            background: linear-gradient(135deg, #5B4BDE 0%, #4A3BC7 50%, #382F93 100%) !important;
            color: white !important;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: rgba(56, 47, 147, 0.9) !important;
            backdrop-filter: blur(10px);
        }
        
        .css-1d391kg .stSelectbox label,
        .css-1d391kg .stTextInput label,
        .css-1d391kg .stSlider label,
        .css-1d391kg .stMultiSelect label,
        .css-1d391kg h1,
        .css-1d391kg h2,
        .css-1d391kg h3,
        .css-1d391kg p {
            color: white !important;
        }
        
        /* Títulos y headers */
        h1, h2, h3, h4, h5, h6 {
            color: white !important;
            font-weight: 700 !important;
        }
        
        /* Texto general */
        p, span, div {
            color: white !important;
        }
        
        /* Botones principales */
        .stButton > button {
            background: white !important;
            color: #382F93 !important;
            border: none !important;
            border-radius: 25px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        }
        
        .stButton > button:hover {
            background: #f0f0f0 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* Métricas */
        .css-1xarl3l {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 15px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .css-1xarl3l [data-testid="metric-container"] {
            color: white !important;
        }
        
        /* Cajas de input */
        .stTextInput input,
        .stSelectbox select,
        .stMultiSelect > div {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput input::placeholder {
            color: rgba(255, 255, 255, 0.7) !important;
        }
        
        /* Sliders */
        .stSlider > div > div > div > div {
            background: rgba(255, 255, 255, 0.3) !important;
        }
        
        .stSlider > div > div > div > div > div {
            background: white !important;
        }
        
        /* Progress bars */
        .stProgress > div > div > div {
            background: white !important;
        }
        
        /* Success/Error/Info messages */
        .stSuccess {
            background: rgba(34, 197, 94, 0.2) !important;
            border: 1px solid rgba(34, 197, 94, 0.4) !important;
            color: #86efac !important;
            border-radius: 10px !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.2) !important;
            border: 1px solid rgba(239, 68, 68, 0.4) !important;
            color: #fca5a5 !important;
            border-radius: 10px !important;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.2) !important;
            border: 1px solid rgba(59, 130, 246, 0.4) !important;
            color: #93c5fd !important;
            border-radius: 10px !important;
        }
        
        .stWarning {
            background: rgba(245, 158, 11, 0.2) !important;
            border: 1px solid rgba(245, 158, 11, 0.4) !important;
            color: #fcd34d !important;
            border-radius: 10px !important;
        }
        
        /* Tablas/DataFrames */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background: rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        .streamlit-expanderContent {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 0 0 10px 10px !important;
        }
        
        /* File uploader */
        .stFileUploader > div {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 2px dashed rgba(255, 255, 255, 0.3) !important;
            border-radius: 15px !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stFileUploader label {
            color: white !important;
        }
        
        /* Dividers */
        hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Columns spacing */
        .css-1kyxreq {
            gap: 2rem;
        }
        
        /* Links */
        a {
            color: #93c5fd !important;
        }
        
        a:hover {
            color: #bfdbfe !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Aplicar tema
apply_spotly_theme()

# ==================== NAVBAR ACTUALIZADO ====================
import base64

def load_logo_base64(path="assets/bg_logo.png"):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        # Si no existe el logo, usar un placeholder
        return ""

def navbar():
    logo_base64 = load_logo_base64()
    
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" alt="Logo">' if logo_base64 else '<div class="logo-placeholder">BD</div>'

    st.markdown(f"""
        <style>
        .navbar {{
            background: rgba(56, 47, 147, 0.9);
            backdrop-filter: blur(10px);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: white;
            position: sticky;
            top: 0;
            z-index: 100;
            border-radius: 0 0 15px 15px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}
        .navbar-left {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}
        .navbar-left img {{
            height: 48px;
            border-radius: 8px;
        }}
        .logo-placeholder {{
            width: 48px;
            height: 48px;
            background: linear-gradient(45deg, #8B5CF6, #EC4899);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
            color: white;
        }}
        .navbar-left h2 {{
            margin: 0;
            font-size: 1.4rem;
            font-weight: 700;
            color: white;
            background: linear-gradient(135deg, #FFFFFF 0%, #E5E7EB 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .nav-links {{
            display: flex;
            gap: 2.5rem;
        }}
        .nav-link {{
            color: white !important; 
            text-decoration: none;
            font-weight: 500;
            font-size: 1rem;
            opacity: 0.9;
            transition: all 0.3s ease;
            padding: 0.5rem 1rem;
            border-radius: 20px;
        }}
        .nav-link:hover {{
            opacity: 1;
            background: rgba(255, 255, 255, 0.1);
        }}
        </style>

        <div class="navbar">
            <div class="navbar-left">
                {logo_html}
                <h2>Brand Detection System</h2>
            </div>
            <div class="nav-links">
                <a class="nav-link" href="?page=home" target="_self">Inicio</a>
                <a class="nav-link" href="?page=analysis" target="_self">Análisis de Video</a>
                <a class="nav-link" href="?page=diagnostic" target="_self">Diagnóstico</a>
                <a class="nav-link" href="?page=explorer" target="_self">Explorador API</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==================== INICIALIZACIÓN ====================
if 'api_client' not in st.session_state:
    st.session_state.api_client = None

# Sidebar - Configuración
st.sidebar.title("⚙️ Configuración")

backend_url = st.sidebar.text_input(
    "URL del Backend",
    value="http://localhost:8000",
    help="URL donde está corriendo tu servidor FastAPI"
)

# Crear/actualizar cliente API
if st.session_state.api_client is None or st.session_state.api_client.base_url != backend_url:
    st.session_state.api_client = BrandDetectionAPI(backend_url)

api = st.session_state.api_client

# Verificar conexión
is_connected = api.health_check()

if is_connected:
    st.sidebar.success("🟢 Backend Conectado")
else:
    st.sidebar.error("🔴 Backend Desconectado")

# ==================== NAVEGACIÓN ====================
query_params = st.query_params
current_page = query_params.get("page", "home")

navbar()

# ==================== PÁGINA: INICIO ====================
if current_page == "home":
    # Hero Section
    st.markdown("""
        <div style="text-align: center; padding: 3rem 0;">
            <h1 style="font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; 
                       background: linear-gradient(135deg, #FFFFFF 0%, #E5E7EB 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                       background-clip: text;">
                Detecta marcas<br>en segundos con IA
            </h1>
            <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem; max-width: 600px; 
                      margin-left: auto; margin-right: auto;">
                Nuestro sistema identifica y rastrea logos en videos e imágenes instantáneamente 
                usando inteligencia artificial avanzada.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Estado del Sistema")
        
        if is_connected:
            st.success("✅ Sistema operativo - el backend está corriendo correctamente")
            
            server_info = api.get_server_info()
            st.subheader("🖥️ Información del Servidor")
            st.write(f"**Status Code:** {server_info.get('status', 'N/A')}")
            if 'headers' in server_info:
                server_type = server_info['headers'].get('server', 'FastAPI')
                st.write(f"**Servidor:** {server_type}")
        else:
            st.error("❌ Sistema desconectado - no se puede conectar con el backend")
            
            st.subheader("🔧 Posibles soluciones")
            st.markdown("""
            1. **Verifica que el backend esté corriendo:**
               ```bash
               cd server
               uvicorn main:app --reload
               ```
            2. **Confirma la URL:** http://localhost:8000  
            3. **Revisa errores** en la consola del backend
            """)
    
    with col2:
        st.subheader("✨ Funcionalidades principales")
        
        features = [
            "🎥 Análisis de videos en tiempo real",
            "🏷️ Detección de múltiples marcas",
            "📈 Reportes detallados",
            "🎚️ Configuración de umbral de confianza",
            "📊 Métricas de rendimiento",
            "💾 Exportación de resultados"
        ]
        
        for feature in features:
            st.markdown(f"**{feature}**")
        
        if is_connected:
            st.success("🚀 Todo listo para comenzar")
        else:
            st.warning("⚠️ Conecta el backend para iniciar")

# ==================== PÁGINA: ANÁLISIS DE VIDEO ====================
elif current_page == "analysis":
    if not is_connected:
        st.error("❌ Backend no conectado")
        st.info("🔌 Conecta primero el backend para usar esta funcionalidad")
        st.stop()
    
    st.header("🎥 Subir y Analizar Video")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "📁 Selecciona tu video",
            type=['mp4', 'avi', 'mov', 'mkv'],
            help="Formatos soportados: MP4, AVI, MOV, MKV (máx. 500MB)"
        )
        
        if uploaded_file is not None:
            is_valid, message = validate_video_file(uploaded_file)
            
            if is_valid:
                st.success(f"✅ {message}")
                
                st.subheader("📋 Información del Video")
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("📄 Archivo", uploaded_file.name)
                with col_b:
                    st.metric("📏 Tamaño", format_file_size(uploaded_file.size))
                with col_c:
                    st.metric("🎬 Tipo", uploaded_file.type.split('/')[-1].upper())
            else:
                st.error(f"❌ {message}")
    
    with col2:
        st.subheader("⚙️ Configuración del Análisis")
        
        confidence_threshold = st.slider(
            "🎯 Umbral de Confianza",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.05,
            help="Nivel de confianza mínimo para considerar una detección válida"
        )
        
        available_brands = ["Apple", "Nike", "McDonald's", "Coca-Cola", "Samsung", "Adidas"]
        selected_brands = st.multiselect(
            "🏷️ Marcas a Detectar",
            available_brands,
            default=["Apple", "Nike"],
            help="Selecciona las marcas que quieres detectar en el video"
        )
        
        process_button = st.button(
            "🚀 Procesar Video", 
            type="primary",
            disabled=uploaded_file is None or not selected_brands,
            help="Inicia el análisis del video con la configuración seleccionada"
        )
    
    if process_button and uploaded_file is not None and selected_brands:
        st.subheader("⚡ Procesando Video...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            ("📤 Enviando video al servidor...", 20),
            ("🤖 Aplicando modelo de detección...", 50),
            ("📊 Analizando resultados...", 80),
            ("✅ Procesamiento completado", 100)
        ]
        
        for stage_text, progress in stages:
            status_text.text(stage_text)
            progress_bar.progress(progress)
            time.sleep(1)
        
        result = api.upload_video(
            uploaded_file,
            confidence_threshold=confidence_threshold,
            brands=selected_brands
        )
        
        if result.get('success', False):
            st.success("🎉 Video procesado exitosamente")
            
            st.subheader("📈 Resultados del Análisis")
            data = result.get('data', {})
            endpoint_used = result.get('endpoint_used', 'Unknown')
            st.info(f"🔗 Endpoint utilizado: {endpoint_used}")
            
            detections_count = len(data.get('detections', [])) if isinstance(data.get('detections'), list) else 0
            st.metric("🎯 Detecciones Encontradas", detections_count)
            
            if data.get('detections') and isinstance(data.get('detections'), list):
                st.subheader("📋 Detecciones Encontradas")
                try:
                    df_detections = pd.DataFrame(data['detections'])
                    st.dataframe(df_detections, use_container_width=True)
                except Exception as e:
                    st.error(f"❌ Error al procesar detecciones: {str(e)}")
                    st.json(data.get('detections'))
            
            with st.expander("🔍 Ver respuesta completa del backend"):
                st.json(result)
        else:
            st.error("❌ Error en el procesamiento")
            error_msg = result.get('error', 'Error desconocido')
            st.error(f"Error: {error_msg}")

# ==================== PÁGINA: DIAGNÓSTICO ====================
elif current_page == "diagnostic":
    st.header("🔧 Diagnóstico del Sistema")
    
    if st.button("🔍 Probar Conexión Básica"):
        with st.spinner("⏳ Probando conexión..."):
            server_info = api.get_server_info()
            time.sleep(1)
        
        if 'error' in server_info:
            st.error(f"❌ Error: {server_info['error']}")
        else:
            st.success(f"✅ Conexión exitosa - Status: {server_info['status']}")
            st.json(server_info)

    if st.button("🗺️ Descubrir Endpoints Disponibles"):
        with st.spinner("🔍 Explorando endpoints..."):
            endpoints = api.discover_endpoints()
            time.sleep(1)
        
        if endpoints:
            st.success(f"✅ Encontrados {len(endpoints)} endpoints")
            st.write(endpoints)
        else:
            st.warning("⚠️ No se encontraron endpoints")

# ==================== PÁGINA: EXPLORADOR DE API ====================
elif current_page == "explorer":
    st.header("🔍 Explorador de API")
    
    if not is_connected:
        st.warning("⚠️ Backend no conectado - algunas funciones pueden no estar disponibles")
    
    st.subheader("🖥️ Información del Servidor")
    server_info = api.get_server_info()
    st.json(server_info)
    
    st.subheader("📚 Documentación Automática")
    st.info("FastAPI genera documentación automática para tu API:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**[📊 Swagger UI]({backend_url}/docs)**")
    with col2:
        st.markdown(f"**[📖 ReDoc]({backend_url}/redoc)**") 
    with col3:
        st.markdown(f"**[📄 OpenAPI JSON]({backend_url}/openapi.json)**")

# ==================== FOOTER ====================
st.divider()
st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.05); 
                border-radius: 15px; margin-top: 2rem; backdrop-filter: blur(10px);">
        <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
            <strong>🎯 Brand Detection System</strong>
        </p>
        <p style="opacity: 0.8; margin: 0;">
            Desarrollado con ❤️ usando Streamlit + FastAPI
        </p>
    </div>
""", unsafe_allow_html=True)