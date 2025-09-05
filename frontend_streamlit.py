import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import base64

# Configuración de la página
st.set_page_config(
    page_title="Spotly - Brand Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL del backend
API_BASE_URL = "http://localhost:8000"

# Estilos CSS con la paleta de Spotly
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --spotly-purple: #8B5CF6;
        --spotly-dark-purple: #7C3AED;
        --spotly-blue: #3B82F6;
        --spotly-dark-blue: #1E40AF;
        --spotly-gradient: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
        --spotly-dark-gradient: linear-gradient(135deg, #7C3AED 0%, #1E40AF 100%);
        --dark-bg: #0F0F23;
        --card-bg: #1A1A2E;
        --text-light: #E2E8F0;
        --text-gray: #94A3B8;
    }
    
    /* Fondo principal */
    .stApp {
        background: var(--dark-bg);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header principal */
    .spotly-header {
        background: var(--spotly-gradient);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);
    }
    
    .spotly-logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .spotly-tagline {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        font-weight: 500;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: var(--text-light);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(139, 92, 246, 0.4);
        border-color: var(--spotly-purple);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: var(--spotly-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-label {
        color: var(--text-gray);
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Cards de contenido */
    .content-card {
        background: var(--card-bg);
        padding: 5px;
        border-radius: 16px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        color: var(--text-light);
    }
    
    /* Success/Error boxes */
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        border: none;
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    
    .error-box {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        border: none;
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }
    
    .info-box {
        background: var(--card-bg);
        border: 1px solid var(--spotly-purple);
        border-radius: 12px;
        padding: 1.5rem;
        color: var(--text-light);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.2);
    }
    
    /* Video cards */
    .video-card {
        background: var(--card-bg);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(139, 92, 246, 0.2);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        color: var(--text-light);
    }
    
    .video-card:hover {
        border-color: var(--spotly-purple);
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3);
    }
    
    /* Progress bar personalizada */
    .stProgress > div > div > div > div {
        background: var(--spotly-gradient);
        border-radius: 10px;
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background: var(--card-bg);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
        color: var(--text-light);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--spotly-purple);
        box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2);
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: var(--text-light);
        font-weight: 600;
    }
    
    /* Texto */
    p, span, div {
        color: var(--text-light);
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        background: var(--card-bg);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Funciones para conectar con la API
@st.cache_data(ttl=30)
def fetch_videos():
    try:
        response = requests.get(f"{API_BASE_URL}/videos/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

@st.cache_data(ttl=30)
def fetch_brands():
    try:
        response = requests.get(f"{API_BASE_URL}/brands/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

@st.cache_data(ttl=30)
def fetch_detections():
    try:
        response = requests.get(f"{API_BASE_URL}/detections/")
        if response.status_code == 200:
            return response.json()
        return []
    except:
        return []

def process_video_url(video_url):
    try:
        response = requests.post(
            f"{API_BASE_URL}/process-video-url/",
            json={"video_url": video_url},
            timeout=300
        )
        return response.status_code == 200, response.json() if response.status_code == 200 else response.text
    except Exception as e:
        return False, str(e)

# Header principal con branding de Spotly
def get_logo_base64(logo_path):
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None

logo_base64 = get_logo_base64("logo.png")  # Cambia por tu archivo

if logo_base64:
    st.markdown(f"""
    <div class="spotly-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" width="200" style="margin-right: 1rem;">
        </div>
        <div class="spotly-tagline">Detect brands in seconds with AI</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Header sin logo si no se encuentra el archivo
    st.markdown("""
    <div class="spotly-header">
        <div class="spotly-logo">SPOTLY</div>
        <div class="spotly-tagline">Detect brands in seconds with AI</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para navegación
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem; margin-bottom: 2rem;">
    <div style="font-size: 1.5rem; font-weight: 600; background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Navigation
    </div>
</div>
""", unsafe_allow_html=True)

# Corregir el selectbox con label visible
page = st.sidebar.selectbox(
    "Choose page",
    ["🏠 Dashboard", "⚡ Process Video", "📹 Videos", "🏷️ Brands"],
    index=0,
    label_visibility="hidden"
)

# Cargar datos
videos = fetch_videos()
brands = fetch_brands()
detections = fetch_detections()

# Funciones auxiliares
def get_video_stats(video_id):
    video_detections = [d for d in detections if d['video_id'] == video_id]
    unique_brands = len(set(d['brand_id'] for d in video_detections))
    total_detections = len(video_detections)
    avg_confidence = 0
    if video_detections:
        avg_confidence = sum(d.get('confidence', 0) for d in video_detections) / len(video_detections) * 100
    return unique_brands, total_detections, round(avg_confidence, 1)

def get_brand_stats():
    brand_counts = {}
    for detection in detections:
        brand = next((b for b in brands if b['id'] == detection['brand_id']), None)
        if brand:
            brand_counts[brand['name']] = brand_counts.get(brand['name'], 0) + 1
    return sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:5]

# PÁGINA: DASHBOARD
if page == "🏠 Dashboard":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Analytics Dashboard")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Videos</div>
            <div class="metric-value">{len(videos)}</div>
            <div style="color: #10B981; font-size: 0.8rem; margin-top: 0.5rem;">
                📹 Processed
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Brands Detected</div>
            <div class="metric-value">{len(brands)}</div>
            <div style="color: #8B5CF6; font-size: 0.8rem; margin-top: 0.5rem;">
                🏷️ Unique
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Detections</div>
            <div class="metric-value">{len(detections)}</div>
            <div style="color: #3B82F6; font-size: 0.8rem; margin-top: 0.5rem;">
                🔍 Found
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        avg_confidence = 0
        if detections:
            avg_confidence = sum(d.get('confidence', 0) for d in detections) / len(detections) * 100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Confidence</div>
            <div class="metric-value">{avg_confidence:.1f}%</div>
            <div style="color: #F59E0B; font-size: 0.8rem; margin-top: 0.5rem;">
                📈 Accuracy
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Top Brands")
        top_brands = get_brand_stats()
        if top_brands:
            df_brands = pd.DataFrame(top_brands, columns=['Brand', 'Detections'])
            fig = px.bar(
                df_brands, 
                x='Detections', 
                y='Brand',
                orientation='h',
                color='Detections',
                color_continuous_scale=[[0, '#8B5CF6'], [1, '#3B82F6']],
                template='plotly_dark'
            )
            fig.update_layout(
                height=400, 
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#E2E8F0')
            )
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No brand data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Confidence Distribution")
        if detections:
            confidences = [d.get('confidence', 0) * 100 for d in detections if d.get('confidence')]
            if confidences:
                fig = px.histogram(
                    x=confidences,
                    nbins=20,
                    title="",
                    labels={'x': 'Confidence (%)', 'y': 'Frequency'},
                    color_discrete_sequence=['#8B5CF6'],
                    template='plotly_dark'
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0')
                )
                st.plotly_chart(fig, width='stretch')
            else:
                st.info("No confidence data available")
        else:
            st.info("No detection data available")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Videos recientes
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 🕒 Recent Videos")
    if videos:
        for video in videos[:5]:
            unique_brands, total_detections, avg_conf = get_video_stats(video['id'])
            
            st.markdown(f"""
            <div class="video-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">
                            📹 {video['filename'][:50]}{'...' if len(video['filename']) > 50 else ''}
                        </div>
                        <div style="color: #94A3B8; font-size: 0.9rem;">
                            🏷️ {unique_brands} brands • 🔍 {total_detections} detections • 📈 {avg_conf}% confidence
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                            ID: {video['id']}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <div style="text-align: center;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📹</div>
                <div style="font-size: 1.2rem; font-weight: 600;">No videos processed yet</div>
                <div style="margin-top: 0.5rem; color: #94A3B8;">Process your first video to see analytics here</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PÁGINA: PROCESAR VIDEO
elif page == "⚡ Process Video":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## ⚡ Process Video from URL")
    st.markdown("Spotly identifies and tracks logos across videos & images instantly.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.form("video_form"):
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📥 Video URL")
        # Corregir el text_input con label visible
        video_url = st.text_input(
            "Enter video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Supports YouTube, Vimeo and other platforms compatible with yt-dlp",
            label_visibility="hidden"
        )
        
        submitted = st.form_submit_button(
            "🚀 Start Detection",
            help="Process video with AI brand detection"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted and video_url:
            with st.spinner("Processing video... This may take several minutes"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simular progreso
                for i in range(100):
                    progress_bar.progress(i + 1)
                    if i < 20:
                        status_text.text("🔽 Downloading video...")
                    elif i < 40:
                        status_text.text("🎬 Extracting frames...")
                    elif i < 80:
                        status_text.text("🔍 Detecting brands...")
                    else:
                        status_text.text("💾 Saving results...")
                    time.sleep(0.1)
                
                success, result = process_video_url(video_url)
                
                if success:
                    st.markdown(f"""
                    <div class="success-box">
                        <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">
                            ✅ Video processed successfully!
                        </div>
                        <div><strong>Video ID:</strong> {result.get('video_id', 'N/A')}</div>
                        <div><strong>Frames processed:</strong> {result.get('frames_processed', 'N/A')}</div>
                        <div><strong>Filename:</strong> {result.get('filename', 'N/A')}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <div style="font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem;">
                            ❌ Processing failed
                        </div>
                        <div>{result}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Información
    st.markdown("""
    <div class="info-box">
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem;">ℹ️ How it works</div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div>
                <div style="font-weight: 600; color: #8B5CF6;">🔍 Brand Detection</div>
                <div style="font-size: 0.9rem; color: #94A3B8;">Accurately identify logos in any video or image</div>
            </div>
            <div>
                <div style="font-weight: 600; color: #3B82F6;">📊 Analytics</div>
                <div style="font-size: 0.9rem; color: #94A3B8;">Get detailed reports on logo appearances and screen time</div>
            </div>
            <div>
                <div style="font-weight: 600; color: #10B981;">⚡ Easy Integration</div>
                <div style="font-size: 0.9rem; color: #94A3B8;">Integrate our API seamlessly with your existing workflow</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# PÁGINA: VIDEOS
elif page == "📹 Videos":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## 📹 Processed Videos")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if videos:
        # Filtros
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Filters")
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("Search by filename:", "")
        
        with col2:
            min_detections = st.number_input("Minimum detections:", min_value=0, value=0)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Filtrar videos
        filtered_videos = videos
        if search_term:
            filtered_videos = [v for v in filtered_videos if search_term.lower() in v['filename'].lower()]
        
        if min_detections > 0:
            filtered_videos = [v for v in filtered_videos if get_video_stats(v['id'])[1] >= min_detections]
        
        # Mostrar videos
        st.markdown(f'<div class="content-card"><h3>📹 Videos ({len(filtered_videos)})</h3></div>', unsafe_allow_html=True)
        
        for video in filtered_videos:
            unique_brands, total_detections, avg_conf = get_video_stats(video['id'])
            
            st.markdown(f"""
            <div class="video-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div style="font-weight: 600; font-size: 1.2rem;">
                        📹 {video['filename'][:60]}{'...' if len(video['filename']) > 60 else ''}
                    </div>
                    <div style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem;">
                        ID: {video['id']}
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
                    <div style="text-align: center; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px; border: 1px solid rgba(139, 92, 246, 0.2);">
                        <div style="font-size: 1.5rem; font-weight: 600; color: #8B5CF6;">{unique_brands}</div>
                        <div style="font-size: 0.8rem; color: #94A3B8;">Brands</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.2);">
                        <div style="font-size: 1.5rem; font-weight: 600; color: #3B82F6;">{total_detections}</div>
                        <div style="font-size: 0.8rem; color: #94A3B8;">Detections</div>
                    </div>
                    <div style="text-align: center; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2);">
                        <div style="font-size: 1.5rem; font-weight: 600; color: #10B981;">{avg_conf}%</div>
                        <div style="font-size: 0.8rem; color: #94A3B8;">Confidence</div>
                    </div>
                </div>
                
                {f'<div style="color: #3B82F6; font-size: 0.9rem;"><a href="{video.get("url", "")}" target="_blank" style="color: #3B82F6; text-decoration: none;">🔗 View original video</a></div>' if video.get('url') else ''}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <div style="text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📹</div>
                <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">No videos processed yet</div>
                <div style="color: #94A3B8;">Go to 'Process Video' to get started with brand detection</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# PÁGINA: MARCAS
elif page == "🏷️ Brands":
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("## 🏷️ Detected Brands")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh"):
            st.cache_data.clear()
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    if brands:
        # Estadísticas de marcas
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Brand Statistics")
        
        brand_data = []
        for brand in brands:
            brand_detections = [d for d in detections if d['brand_id'] == brand['id']]
            avg_confidence = 0
            if brand_detections:
                avg_confidence = sum(d.get('confidence', 0) for d in brand_detections) / len(brand_detections) * 100
            
            brand_data.append({
                'ID': brand['id'],
                'Brand': brand['name'],
                'Detections': len(brand_detections),
                'Avg Confidence (%)': round(avg_confidence, 1)
            })
        
        df = pd.DataFrame(brand_data)
        
        # Mostrar tabla
        st.dataframe(
            df,
            column_config={
                'ID': st.column_config.NumberColumn('ID', width=80),
                'Brand': st.column_config.TextColumn('Brand', width=200),
                'Detections': st.column_config.NumberColumn('Detections', width=120),
                'Avg Confidence (%)': st.column_config.ProgressColumn(
                    'Confidence (%)',
                    min_value=0,
                    max_value=100,
                    width=200
                )
            },
            hide_index=True,
            width='stretch'
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Gráficos de marcas
        if len(df) > 0:
            st.markdown('<div class="content-card">', unsafe_allow_html=True)
            st.markdown("### 📈 Brand Visualizations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_detections = px.bar(
                    df.sort_values('Detections', ascending=False).head(10),
                    x='Brand',
                    y='Detections',
                    title="Top 10 Brands by Detections",
                    color='Detections',
                    color_continuous_scale=[[0, '#8B5CF6'], [1, '#3B82F6']],
                    template='plotly_dark'
                )
                fig_detections.update_xaxes(tickangle=45)
                fig_detections.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0')
                )
                st.plotly_chart(fig_detections, width='stretch')
            
            with col2:
                fig_confidence = px.scatter(
                    df,
                    x='Detections',
                    y='Avg Confidence (%)',
                    size='Detections',
                    hover_name='Brand',
                    title="Detections vs Confidence",
                    color='Avg Confidence (%)',
                    color_continuous_scale=[[0, '#8B5CF6'], [1, '#3B82F6']],
                    template='plotly_dark'
                )
                fig_confidence.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#E2E8F0')
                )
                st.plotly_chart(fig_confidence, width='stretch')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Mostrar marcas en grid
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🏷️ Brand Gallery")
        
        # Crear grid de marcas
        brands_per_row = 3
        for i in range(0, len(brand_data), brands_per_row):
            cols = st.columns(brands_per_row)
            for j in range(brands_per_row):
                if i + j < len(brand_data):
                    brand = brand_data[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div style="
                            background: var(--card-bg);
                            padding: 1.5rem;
                            border-radius: 12px;
                            border: 1px solid rgba(139, 92, 246, 0.2);
                            text-align: center;
                            transition: all 0.3s ease;
                            margin-bottom: 1rem;
                        ">
                            <div style="font-size: 2rem; margin-bottom: 1rem;">🏷️</div>
                            <div style="font-weight: 600; font-size: 1.2rem; margin-bottom: 0.5rem; color: #E2E8F0;">
                                {brand['Brand']}
                            </div>
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span style="color: #94A3B8; font-size: 0.9rem;">Detections:</span>
                                <span style="color: #8B5CF6; font-weight: 600;">{brand['Detections']}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between;">
                                <span style="color: #94A3B8; font-size: 0.9rem;">Confidence:</span>
                                <span style="color: #10B981; font-weight: 600;">{brand['Avg Confidence (%)']}%</span>
                            </div>
                            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(139, 92, 246, 0.1); border-radius: 6px; font-size: 0.8rem; color: #94A3B8;">
                                ID: {brand['ID']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="info-box">
            <div style="text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🏷️</div>
                <div style="font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">No brands detected yet</div>
                <div style="color: #94A3B8;">Process some videos to see detected brands here</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 2rem; color: #94A3B8;">
    <div style="font-size: 1.5rem; font-weight: 600; background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;">
        SPOTLY
    </div>
    <div style="font-size: 0.9rem;">
        Brand Detection System | Backend: {'🟢 Connected' if videos is not None else '🔴 Disconnected'}
    </div>
    <div style="font-size: 0.8rem; margin-top: 0.5rem; color: #64748B;">
        Detect brands in seconds with AI • Computer Vision Project
    </div>
</div>
""", unsafe_allow_html=True)