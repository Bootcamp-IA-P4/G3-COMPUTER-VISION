import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import base64
from io import BytesIO
from typing import List, Dict, Any, Optional

# Configuración de colores profesionales
BRAND_COLORS = {
    'primary': '#0066cc',
    'primary_dark': '#004499',
    'secondary': '#ff6b35',
    'accent': '#00d4aa',
    'success': '#10b981',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'text_primary': '#1a1a1a',
    'text_secondary': '#666666',
    'background_light': '#f8fafc',
    'background_card': '#ffffff',
    'border': '#e5e7eb'
}

COLOR_PALETTE = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a', '#ffcc70', '#70d0e4']

def init_session_state():
    """Inicializa el estado de sesión con valores por defecto profesionales"""
    defaults = {
        'api_client': None,
        'current_page': 'Dashboard',
        'user_settings': {
            'default_confidence': 0.5,
            'selected_brands': ['Apple', 'Nike', 'Samsung'],
            'theme': 'Professional Blue',
            'auto_refresh': False,
            'animations_enabled': True
        },
        'analysis_history': [],
        'last_analysis_result': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def create_professional_metric_card(title: str, value: str, change: str = None, 
                                  change_type: str = "neutral", icon: str = None):
    """Crea una tarjeta de métrica profesional"""
    
    change_colors = {
        'positive': '#10b981',
        'negative': '#ef4444',
        'neutral': '#6b7280'
    }
    
    change_color = change_colors.get(change_type, change_colors['neutral'])
    
    change_html = ""
    if change:
        change_html = f"""
        <div style="
            display: inline-flex; 
            align-items: center; 
            padding: 0.25rem 0.75rem; 
            border-radius: 6px; 
            font-size: 0.75rem; 
            font-weight: 600;
            background: {change_color}20;
            color: {change_color};
            margin-top: 0.5rem;
        ">
            {change}
        </div>
        """
    
    icon_html = ""
    if icon:
        icon_html = f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>'
    
    return f"""
    <div style="
        background: {BRAND_COLORS['background_card']};
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid {BRAND_COLORS['border']};
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 3px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);"></div>
        {icon_html}
        <div style="font-size: 2.5rem; font-weight: 700; color: {BRAND_COLORS['text_primary']}; 
                    margin: 0 0 0.5rem 0; line-height: 1;">
            {value}
        </div>
        <div style="color: {BRAND_COLORS['text_secondary']}; font-size: 0.875rem; 
                    text-transform: uppercase; letter-spacing: 0.1em; font-weight: 500; 
                    margin: 0 0 1rem 0;">
            {title}
        </div>
        {change_html}
    </div>
    """

def create_advanced_timeline_chart(detections: List[Dict], title: str = "Brand Detection Timeline"):
    """Crea un gráfico de timeline avanzado y profesional"""
    if not detections:
        return None
    
    df = pd.DataFrame(detections)
    
    # Crear figura con subplots
    fig = make_subplots(
        rows=2, cols=1,
        row_heights=[0.7, 0.3],
        subplot_titles=('Detection Timeline', 'Confidence Distribution'),
        vertical_spacing=0.1
    )
    
    # Timeline scatter plot
    brands = df['brand'].unique()
    for i, brand in enumerate(brands):
        brand_data = df[df['brand'] == brand]
        
        fig.add_trace(
            go.Scatter(
                x=brand_data['timestamp'],
                y=[brand] * len(brand_data),
                mode='markers',
                marker=dict(
                    size=brand_data['confidence'] * 30,
                    color=COLOR_PALETTE[i % len(COLOR_PALETTE)],
                    opacity=0.8,
                    line=dict(width=2, color='white')
                ),
                name=brand,
                hovertemplate='<b>%{y}</b><br>' +
                             'Time: %{x:.1f}s<br>' +
                             'Confidence: %{customdata:.1%}<br>' +
                             '<extra></extra>',
                customdata=brand_data['confidence'],
                showlegend=True
            ),
            row=1, col=1
        )
    
    # Confidence histogram
    fig.add_trace(
        go.Histogram(
            x=df['confidence'],
            nbinsx=20,
            name='Confidence Distribution',
            marker_color='rgba(102, 126, 234, 0.7)',
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=20, family="Inter, sans-serif", color=BRAND_COLORS['text_primary'])
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        height=600,
        hovermode='closest'
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        title_text="Time (seconds)",
        row=1, col=1
    )
    
    fig.update_yaxes(
        gridcolor='rgba(0,0,0,0.1)',
        gridwidth=1,
        title_text="Brands",
        row=1, col=1
    )
    
    fig.update_xaxes(
        title_text="Confidence Score",
        row=2, col=1
    )
    
    fig.update_yaxes(
        title_text="Frequency",
        row=2, col=1
    )
    
    return fig

def create_brand_performance_chart(summary_data: Dict):
    """Crea un gráfico de rendimiento por marca"""
    if not summary_data:
        return None
    
    brands = list(summary_data.keys())
    total_times = [data.get('total_time', 0) for data in summary_data.values()]
    appearances = [data.get('appearances', 0) for data in summary_data.values()]
    avg_confidence = [data.get('avg_confidence', 0) for data in summary_data.values()]
    
    # Crear subplot con ejes múltiples
    fig = make_subplots(
        specs=[[{"secondary_y": True}]]
    )
    
    # Barras de tiempo total
    fig.add_trace(
        go.Bar(
            name='Total Screen Time (s)',
            x=brands,
            y=total_times,
            marker_color=COLOR_PALETTE[0],
            opacity=0.8,
            yaxis='y'
        ),
        secondary_y=False,
    )
    
    # Línea de apariciones
    fig.add_trace(
        go.Scatter(
            name='Number of Appearances',
            x=brands,
            y=appearances,
            mode='lines+markers',
            line=dict(color=COLOR_PALETTE[2], width=3),
            marker=dict(size=8, color=COLOR_PALETTE[2]),
            yaxis='y2'
        ),
        secondary_y=True,
    )
    
    # Actualizar layout
    fig.update_layout(
        title=dict(
            text='Brand Performance Analysis',
            x=0.5,
            font=dict(size=18, family="Inter, sans-serif")
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif"),
        height=500,
        hovermode='x unified'
    )
    
    # Set y-axes titles
    fig.update_yaxes(title_text="Screen Time (seconds)", secondary_y=False)
    fig.update_yaxes(title_text="Number of Appearances", secondary_y=True)
    
    fig.update_xaxes(title_text="Brands")
    
    return fig

def create_confidence_heatmap(detections: List[Dict]):
    """Crea un mapa de calor de confianzas por marca y tiempo"""
    if not detections:
        return None
    
    df = pd.DataFrame(detections)
    
    # Crear bins de tiempo
    df['time_bin'] = pd.cut(df['timestamp'], bins=10, precision=1)
    
    # Crear pivot table
    heatmap_data = df.groupby(['brand', 'time_bin'])['confidence'].mean().unstack(fill_value=0)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=[f"{interval.left:.1f}-{interval.right:.1f}s" for interval in heatmap_data.columns],
        y=heatmap_data.index,
        colorscale='Blues',
        hoverongaps=False,
        hovertemplate='Brand: %{y}<br>Time: %{x}<br>Avg Confidence: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Confidence Heatmap: Brand Detection Over Time',
        xaxis_title='Time Intervals',
        yaxis_title='Brands',
        font=dict(family="Inter, sans-serif"),
        height=400
    )
    
    return fig

def generate_professional_report(results: Dict, filename: str = None) -> bytes:
    """Genera un reporte profesional en formato Excel"""
    if filename is None:
        filename = f"brand_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Hoja de resumen ejecutivo
        executive_summary = pd.DataFrame([
            {'Metric': 'Total Video Duration', 'Value': f"{results.get('total_duration', 0):.1f} seconds"},
            {'Metric': 'Total Detections Found', 'Value': len(results.get('detections', []))},
            {'Metric': 'Unique Brands Detected', 'Value': len(results.get('summary', {}))},
            {'Metric': 'Average Confidence Score', 'Value': f"{np.mean([d.get('confidence', 0) for d in results.get('detections', [])]) if results.get('detections') else 0:.1%}"},
            {'Metric': 'Processing Date', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')},
            {'Metric': 'Analysis Algorithm', 'Value': 'Advanced Computer Vision ML'}
        ])
        executive_summary.to_excel(writer, sheet_name='Executive Summary', index=False)
        
        # Hoja de detecciones detalladas
        if results.get('detections'):
            detections_df = pd.DataFrame(results['detections'])
            detections_df['Timestamp (MM:SS)'] = detections_df['timestamp'].apply(
                lambda x: f"{int(x//60):02d}:{int(x%60):02d}"
            )
            detections_df['Confidence (%)'] = (detections_df['confidence'] * 100).round(1)
            detections_df = detections_df[['Timestamp (MM:SS)', 'brand', 'Confidence (%)']]
            detections_df.columns = ['Timestamp', 'Brand', 'Confidence (%)']
            detections_df.to_excel(writer, sheet_name='Detailed Detections', index=False)
        
        # Hoja de análisis por marca
        if results.get('summary'):
            brand_analysis = []
            total_duration = results.get('total_duration', 1)
            
            for brand, data in results['summary'].items():
                brand_analysis.append({
                    'Brand': brand,
                    'Total Screen Time (s)': data.get('total_time', 0),
                    'Number of Appearances': data.get('appearances', 0),
                    'Percentage of Video (%)': round((data.get('total_time', 0) / total_duration) * 100, 2),
                    'Average Confidence (%)': round(data.get('avg_confidence', 0) * 100, 1) if data.get('avg_confidence') else 0
                })
            
            brand_df = pd.DataFrame(brand_analysis)
            brand_df = brand_df.sort_values('Total Screen Time (s)', ascending=False)
            brand_df.to_excel(writer, sheet_name='Brand Analysis', index=False)
        
        # Hoja de métricas de rendimiento
        performance_metrics = pd.DataFrame([
            {'Category': 'Detection Performance', 'Metric': 'Total Detections', 'Value': len(results.get('detections', []))},
            {'Category': 'Detection Performance', 'Metric': 'Detections per Minute', 'Value': round(len(results.get('detections', [])) / (results.get('total_duration', 60) / 60), 2)},
            {'Category': 'Accuracy Metrics', 'Metric': 'High Confidence Detections (>80%)', 'Value': len([d for d in results.get('detections', []) if d.get('confidence', 0) > 0.8])},
            {'Category': 'Coverage Analysis', 'Metric': 'Brand Coverage Ratio', 'Value': f"{(len(results.get('summary', {})) / max(len(results.get('target_brands', [])), 1)):.1%}" if results.get('target_brands') else 'N/A'}
        ])
        performance_metrics.to_excel(writer, sheet_name='Performance Metrics', index=False)
    
    return output.getvalue()

def create_status_indicator(status: str, text: str = None) -> str:
    """Crea un indicador de estado profesional"""
    status_config = {
        'online': {'color': '#10b981', 'bg': 'rgba(16, 185, 129, 0.1)', 'icon': '●'},
        'offline': {'color': '#ef4444', 'bg': 'rgba(239, 68, 68, 0.1)', 'icon': '●'},
        'processing': {'color': '#f59e0b', 'bg': 'rgba(245, 158, 11, 0.1)', 'icon': '◐'},
        'warning': {'color': '#f59e0b', 'bg': 'rgba(245, 158, 11, 0.1)', 'icon': '!'},
        'success': {'color': '#10b981', 'bg': 'rgba(16, 185, 129, 0.1)', 'icon': '✓'},
        'error': {'color': '#ef4444', 'bg': 'rgba(239, 68, 68, 0.1)', 'icon': '✗'}
    }
    
    config = status_config.get(status.lower(), status_config['offline'])
    display_text = text or status.title()
    
    return f"""
    <div style="
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem 0;
        background: {config['bg']};
        color: {config['color']};
        border: 1px solid {config['color']}20;
    ">
        <span style="margin-right: 0.5rem; font-size: 1rem;">{config['icon']}</span>
        {display_text}
    </div>
    """

def create_professional_card(title: str, subtitle: str = None, content: str = "", 
                           card_type: str = "default") -> str:
    """Crea una tarjeta profesional con contenido personalizado"""
    
    card_styles = {
        'default': {'border_color': BRAND_COLORS['border'], 'header_bg': 'transparent'},
        'primary': {'border_color': BRAND_COLORS['primary'], 'header_bg': f"{BRAND_COLORS['primary']}10"},
        'success': {'border_color': BRAND_COLORS['success'], 'header_bg': f"{BRAND_COLORS['success']}10"},
        'warning': {'border_color': BRAND_COLORS['warning'], 'header_bg': f"{BRAND_COLORS['warning']}10"},
        'error': {'border_color': BRAND_COLORS['error'], 'header_bg': f"{BRAND_COLORS['error']}10"}
    }
    
    style = card_styles.get(card_type, card_styles['default'])
    
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <p style="color: {BRAND_COLORS['text_secondary']}; margin: 0; font-size: 0.875rem;">
            {subtitle}
        </p>
        """
    
    return f"""
    <div style="
        background: {BRAND_COLORS['background_card']};
        border-radius: 16px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        border: 1px solid {style['border_color']};
        overflow: hidden;
        margin: 1rem 0;
    ">
        <div style="
            padding: 2rem 2rem 0 2rem;
            background: {style['header_bg']};
            border-bottom: 1px solid {BRAND_COLORS['border']};
            margin-bottom: 2rem;
        ">
            <h3 style="
                font-size: 1.5rem;
                font-weight: 600;
                color: {BRAND_COLORS['text_primary']};
                margin: 0 0 0.5rem 0;
            ">{title}</h3>
            {subtitle_html}
        </div>
        <div style="padding: 0 2rem 2rem 2rem;">
            {content}
        </div>
    </div>
    """

def create_progress_bar(progress: float, label: str = "", color: str = None) -> str:
    """Crea una barra de progreso profesional"""
    if color is None:
        color = BRAND_COLORS['primary']
    
    return f"""
    <div style="margin: 1rem 0;">
        <div style="
            display: flex;
            justify-content: space-between;
            margin-bottom: 0.5rem;
        ">
            <span style="font-weight: 500; color: {BRAND_COLORS['text_primary']};">
                {label}
            </span>
            <span style="font-weight: 600; color: {color};">
                {progress:.1%}
            </span>
        </div>
        <div style="
            width: 100%;
            height: 8px;
            background: {BRAND_COLORS['border']};
            border-radius: 4px;
            overflow: hidden;
        ">
            <div style="
                height: 100%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px;
                width: {progress * 100}%;
                transition: width 0.3s ease;
            "></div>
        </div>
    </div>
    """

def format_duration(seconds: float, format_type: str = "long") -> str:
    """Formatea duración con diferentes estilos"""
    if format_type == "short":
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"
    
    else:  # format_type == "long"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"

def validate_file_professional(uploaded_file, max_size_mb: int = 500) -> tuple[bool, str, Dict]:
    """Validación profesional de archivos con información detallada"""
    if not uploaded_file:
        return False, "No file selected", {}
    
    # Información del archivo
    file_info = {
        'name': uploaded_file.name,
        'size': uploaded_file.size,
        'type': uploaded_file.type,
        'size_mb': uploaded_file.size / (1024 * 1024)
    }
    
    # Validaciones
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    file_extension = f".{uploaded_file.name.lower().split('.')[-1]}"
    
    if file_extension not in allowed_extensions:
        return False, f"Unsupported format. Allowed: {', '.join(allowed_extensions)}", file_info
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if uploaded_file.size > max_size_bytes:
        return False, f"File too large. Maximum size: {max_size_mb}MB", file_info
    
    if uploaded_file.size < 1024:  # Menos de 1KB
        return False, "File appears to be corrupted or empty", file_info
    
    return True, "File validation successful", file_info

def create_data_table_professional(df: pd.DataFrame, title: str = None) -> str:
    """Crea una tabla de datos con estilo profesional"""
    table_html = df.to_html(
        index=False,
        classes="professional-table",
        table_id="data-table"
    )
    
    # CSS para la tabla
    table_css = f"""
    <style>
    .professional-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 0.875rem;
        background: {BRAND_COLORS['background_card']};
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }}
    
    .professional-table th {{
        background: {BRAND_COLORS['background_light']};
        padding: 1rem;
        text-align: left;
        font-weight: 600;
        color: {BRAND_COLORS['text_primary']};
        border-bottom: 2px solid {BRAND_COLORS['border']};
    }}
    
    .professional-table td {{
        padding: 0.75rem 1rem;
        border-bottom: 1px solid {BRAND_COLORS['border']};
        color: {BRAND_COLORS['text_secondary']};
    }}
    
    .professional-table tr:hover {{
        background: {BRAND_COLORS['background_light']};
    }}
    </style>
    """
    
    title_html = ""
    if title:
        title_html = f"""
        <h4 style="
            margin: 0 0 1rem 0;
            font-size: 1.25rem;
            font-weight: 600;
            color: {BRAND_COLORS['text_primary']};
        ">{title}</h4>
        """
    
    return f"""
    {table_css}
    <div style="margin: 2rem 0;">
        {title_html}
        {table_html}
    </div>
    """

def get_mock_analytics_data():
    """Genera datos analíticos simulados para demostración"""
    return {
        'daily_detections': {
            'dates': pd.date_range(start='2024-01-01', end='2024-01-30', freq='D'),
            'values': np.random.poisson(25, 30)
        },
        'brand_performance': {
            'Apple': {'detections': 450, 'avg_confidence': 0.94, 'screen_time': 125.5},
            'Nike': {'detections': 320, 'avg_confidence': 0.87, 'screen_time': 98.3},
            'McDonald\'s': {'detections': 280, 'avg_confidence': 0.91, 'screen_time': 76.8},
            'Samsung': {'detections': 210, 'avg_confidence': 0.89, 'screen_time': 65.2},
            'Coca-Cola': {'detections': 180, 'avg_confidence': 0.86, 'screen_time': 54.7}
        },
        'system_metrics': {
            'uptime': 0.987,
            'avg_processing_time': 2.34,
            'success_rate': 0.992,
            'total_videos_processed': 10247
        }
    }

def create_animated_counter(target_value: int, label: str, duration_ms: int = 2000):
    """Crea un contador animado usando JavaScript"""
    counter_id = f"counter_{hash(label) % 10000}"
    
    return f"""
    <div id="{counter_id}" style="text-align: center; padding: 1rem;">
        <div style="font-size: 2.5rem; font-weight: 700; color: {BRAND_COLORS['primary']}; margin-bottom: 0.5rem;">
            0
        </div>
        <div style="color: {BRAND_COLORS['text_secondary']}; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em;">
            {label}
        </div>
    </div>
    
    <script>
    (function() {{
        const element = document.getElementById('{counter_id}').firstElementChild;
        const target = {target_value};
        const duration = {duration_ms};
        const startTime = performance.now();
        
        function animate(currentTime) {{
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function (ease-out)
            const eased = 1 - Math.pow(1 - progress, 3);
            
            const current = Math.floor(eased * target);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {{
                requestAnimationFrame(animate);
            }}
        }}
        
        requestAnimationFrame(animate);
    }})();
    </script>
    """

# Configuraciones de exportación
EXPORT_FORMATS = {
    'excel': {
        'mime_type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'extension': '.xlsx',
        'description': 'Excel Workbook with multiple sheets'
    },
    'csv': {
        'mime_type': 'text/csv',
        'extension': '.csv',
        'description': 'Comma-separated values file'
    },
    'json': {
        'mime_type': 'application/json',
        'extension': '.json',
        'description': 'JSON formatted data file'
    },
    'pdf': {
        'mime_type': 'application/pdf',
        'extension': '.pdf',
        'description': 'Portable Document Format report'
    }
}