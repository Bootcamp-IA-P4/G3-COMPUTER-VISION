import requests
import json
import streamlit as st
from typing import Dict, List, Optional, Union
import time

class BrandDetectionAPI:
    """Cliente para tu backend FastAPI"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json'
        })
    
    def health_check(self) -> bool:
        """Verifica si tu FastAPI está corriendo"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=5)
            return response.status_code in [200, 404]  # 404 también indica que el servidor responde
        except requests.exceptions.ConnectionError:
            return False
        except Exception:
            return False
    
    def get_server_info(self) -> Dict:
        """Obtiene información del servidor"""
        try:
            response = self.session.get(f"{self.base_url}/")
            return {
                'status': response.status_code,
                'content': response.text[:200] if response.text else 'No content',
                'headers': dict(response.headers)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def test_endpoint(self, endpoint: str) -> Dict:
        """Prueba cualquier endpoint de tu backend"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = self.session.get(url, timeout=10)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'success': response.status_code < 400
            }
            
            # Intentar parsear como JSON
            try:
                result['data'] = response.json()
            except:
                result['text'] = response.text[:500]  # Primeros 500 caracteres
            
            return result
            
        except requests.exceptions.ConnectionError:
            return {
                'url': f"{self.base_url}{endpoint}",
                'error': 'Connection refused - ¿Está corriendo tu servidor?',
                'success': False
            }
        except requests.exceptions.Timeout:
            return {
                'url': f"{self.base_url}{endpoint}",
                'error': 'Request timeout',
                'success': False
            }
        except Exception as e:
            return {
                'url': f"{self.base_url}{endpoint}",
                'error': str(e),
                'success': False
            }
    
    def upload_video(self, video_file, **kwargs) -> Dict:
        """
        Sube video para análisis
        NOTA: Este método necesita ser adaptado según tu implementación real
        """
        try:
            files = {
                'file': (video_file.name, video_file.getvalue(), video_file.type)
            }
            
            # Datos adicionales
            data = {}
            if 'confidence_threshold' in kwargs:
                data['confidence_threshold'] = kwargs['confidence_threshold']
            if 'brands' in kwargs:
                data['brands'] = json.dumps(kwargs['brands'])
            
            # Intentar diferentes endpoints posibles
            possible_endpoints = [
                '/upload-video',
                '/analyze-video', 
                '/analyze',
                '/upload',
                '/process-video'
            ]
            
            for endpoint in possible_endpoints:
                try:
                    response = requests.post(
                        f"{self.base_url}{endpoint}",
                        files=files,
                        data=data,
                        timeout=300  # 5 minutos para videos largos
                    )
                    
                    if response.status_code == 200:
                        return {
                            'success': True,
                            'endpoint_used': endpoint,
                            'data': response.json()
                        }
                    elif response.status_code == 404:
                        continue  # Probar siguiente endpoint
                    else:
                        return {
                            'success': False,
                            'endpoint_used': endpoint,
                            'status_code': response.status_code,
                            'error': response.text
                        }
                        
                except requests.exceptions.ConnectionError:
                    continue
                except Exception as e:
                    continue
            
            return {
                'success': False,
                'error': f'No se encontró endpoint de upload válido en: {possible_endpoints}',
                'suggestion': 'Verifica que tu backend tenga un endpoint para subir videos'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            }
    
    def discover_endpoints(self) -> List[str]:
        """Intenta descubrir endpoints disponibles"""
        common_endpoints = [
            '/',
            '/docs',
            '/openapi.json',
            '/health',
            '/status',
            '/ping',
            '/upload',
            '/analyze',
            '/video',
            '/brands',
            '/results'
        ]
        
        available = []
        for endpoint in common_endpoints:
            result = self.test_endpoint(endpoint)
            if result.get('success', False) or result.get('status_code', 500) != 404:
                available.append(endpoint)
        
        return available

def format_file_size(size_bytes: int) -> str:
    """Convierte bytes a formato legible"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def validate_video_file(uploaded_file) -> tuple[bool, str]:
    """Valida el archivo de video subido"""
    if not uploaded_file:
        return False, "No se ha seleccionado ningún archivo"
    
    # Verificar extensión
    allowed_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
    file_extension = uploaded_file.name.lower().split('.')[-1]
    if f'.{file_extension}' not in allowed_extensions:
        return False, f"Formato no soportado. Usa: {', '.join(allowed_extensions)}"
    
    # Verificar tamaño (máximo 500MB por defecto)
    max_size = 500 * 1024 * 1024  # 500MB en bytes
    if uploaded_file.size > max_size:
        return False, f"Archivo muy grande. Máximo: {format_file_size(max_size)}"
    
    return True, "Archivo válido"