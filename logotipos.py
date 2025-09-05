import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random

# 1. Configurar el navegador Chrome
options = Options()
options.add_argument("--headless")  # Comentado para poder ver el navegador en acción
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")  # Evitar detección de automatización
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

# Configurar un User-Agent realista
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

# Función para extraer el nombre de la marca desde la URL del logotipo
def extraer_nombre_marca(url):
    try:
        # Eliminar extensiones comunes
        nombre = url.lower()
        for ext in ['.png', '.svg', '.jpg', '.jpeg']:
            nombre = nombre.replace(ext, '')
            
        # Eliminar dominios y rutas comunes
        if '/' in nombre:
            nombre = nombre.split('/')[-1]
            
        # Limpiar caracteres especiales y palabras comunes
        nombre = nombre.replace('-', ' ').replace('_', ' ')
        palabras_a_eliminar = ['logo', 'brand', 'icon', 'symbol']
        for palabra in palabras_a_eliminar:
            nombre = nombre.replace(palabra, '')
            
        # Limpiar espacios extra y capitalizar
        nombre = ' '.join(nombre.split()).strip().title()
        
        return nombre if nombre else "Desconocido"
    except:
        return "Desconocido"

# Función para extraer URLs de logotipos de la página actual
def extraer_logos_de_pagina(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    image_tags = soup.find_all('img')
    
    urls_encontradas = []
    for img in image_tags:
        src = img.get('src')
        if src:
            if src.endswith(('.png', '.svg', '.jpg', '.jpeg')) and 'logo' in src:
                urls_encontradas.append(src)
    
    return urls_encontradas

# Función para manejar popups y overlays
def manejar_popups(driver):
    try:
        # Intentar cerrar el overlay de cookies (fc-dialog-overlay)
        overlay = driver.find_element(By.CLASS_NAME, "fc-dialog-overlay")
        if overlay:
            print("Detectado overlay de cookies. Intentando cerrar...")
            # Buscar botones de aceptar cookies
            accept_buttons = [
                ".fc-button-label",  # Selector común para botones de cookies
                ".fc-primary-button",
                "#onetrust-accept-btn-handler",
                ".accept-cookies",
                ".cookie-accept",
                "button[aria-label='Aceptar cookies']",
                "button:contains('Accept')",
                "button:contains('Aceptar')"
            ]
            
            for selector in accept_buttons:
                try:
                    # Intentar diferentes métodos de selección
                    try:
                        button = driver.find_element(By.CSS_SELECTOR, selector)
                    except:
                        try:
                            button = driver.find_element(By.XPATH, f"//button[contains(text(), 'Accept')]")
                        except:
                            button = driver.find_element(By.XPATH, f"//button[contains(text(), 'Aceptar')]")
                    
                    if button:
                        button.click()
                        print("Botón de cookies clickeado.")
                        time.sleep(1)  # Esperar a que desaparezca el overlay
                        return True
                except:
                    continue
            
            # Si no encontramos un botón específico, intentar hacer clic en el overlay directamente
            try:
                overlay.click()
                print("Overlay clickeado directamente.")
                time.sleep(1)
                return True
            except:
                pass
            
            # Como último recurso, usar JavaScript para eliminar el overlay
            driver.execute_script("arguments[0].remove();", overlay)
            print("Overlay eliminado mediante JavaScript.")
            time.sleep(1)
            return True
    except:
        pass
    
    # Intentar eliminar cualquier overlay mediante JavaScript
    try:
        driver.execute_script("""
        var overlays = document.querySelectorAll('.fc-dialog-overlay, .cookie-banner, .modal, .popup, .overlay');
        for(var i=0; i<overlays.length; i++) {
            overlays[i].remove();
        }
        """)
        print("Eliminados posibles overlays mediante JavaScript.")
        return True
    except:
        pass
    
    return False

try:
    # Inicializar el navegador
    print("Inicializando el navegador Chrome...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Establecer un timeout más largo para las operaciones del navegador
    driver.set_page_load_timeout(180)  # Aumentar a 180 segundos (3 minutos)

    # 2. Definir la URL de la página web inicial
    url_base = 'https://brandlogos.net/brand-logos'
    
    # Variables para controlar la paginación
    pagina_actual = 1
    max_paginas = 577  # Puedes ajustar este valor según necesites
    todas_las_urls = []
    
    while pagina_actual <= max_paginas:
        # Construir la URL de la página actual
        if pagina_actual == 1:
            url = url_base
        else:
            url = f"{url_base}/page/{pagina_actual}"
        
        # Navegar a la página
        print(f"\nAccediendo a la página {pagina_actual}: {url}...")
        driver.get(url)
        
        # Esperar a que la página cargue completamente
        time.sleep(random.uniform(3, 5))
        
        # Manejar popups y overlays antes de continuar
        manejar_popups(driver)
        
        # Obtener el contenido HTML de la página
        html_content = driver.page_source
        
        # Guardar el HTML de cada página para inspección (opcional)
        #with open(f'pagina_{pagina_actual}.html', 'w', encoding='utf-8') as f:
            #f.write(html_content)
        
        # Extraer las URLs de los logotipos de la página actual
        logos_pagina_actual = extraer_logos_de_pagina(html_content)
        print(f"Se encontraron {len(logos_pagina_actual)} URLs de logotipos en la página {pagina_actual}.")
        
        # Añadir las URLs encontradas a la lista general
        todas_las_urls.extend(logos_pagina_actual)
        
        # Verificar si existe un botón "Siguiente" o similar para pasar a la siguiente página
        try:
            # Intentar encontrar el enlace de la siguiente página
            next_button = None
            
            # Intentar diferentes selectores comunes para botones de paginación
            selectors_to_try = [
                "//a[contains(text(), 'Next')]",  # Texto "Next"
                "//a[contains(text(), 'Siguiente')]",  # Texto "Siguiente" en español
                "//a[@class='next page-numbers']",  # Clase común en WordPress
                "//a[@rel='next']",  # Atributo rel="next"
                "//li[@class='pagination-next']/a",  # Estructura común de paginación
                "//a[contains(@class, 'next')]",  # Clase que contiene "next"
                "//a[contains(@class, '_next_page')]",  # Clase específica encontrada en el error
                f"//a[contains(@href, '/page/{pagina_actual + 1}')]",  # URL de la siguiente página
            ]
            
            for selector in selectors_to_try:
                try:
                    next_button = driver.find_element(By.XPATH, selector)
                    if next_button:
                        break
                except NoSuchElementException:
                    continue
            
            if next_button:
                print(f"Botón 'Siguiente' encontrado. Pasando a la página {pagina_actual + 1}...")
                
                # Verificar si hay overlays antes de hacer clic
                manejar_popups(driver)
                
                # Hacer scroll hasta el botón para asegurarnos de que es visible
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                time.sleep(2)  # Pequeña pausa para que el scroll termine
                
                # Intentar hacer clic con diferentes métodos
                try:
                    # Método 1: Clic normal
                    next_button.click()
                except ElementClickInterceptedException:
                    try:
                        # Método 2: Clic con JavaScript
                        driver.execute_script("arguments[0].click();", next_button)
                    except:
                        # Método 3: Navegar directamente a la URL del botón
                        href = next_button.get_attribute('href')
                        if href:
                            driver.get(href)
                
                # Esperar un tiempo aleatorio entre páginas para simular comportamiento humano
                time.sleep(random.uniform(5, 12))
                pagina_actual += 1
            else:
                print("No se encontró botón 'Siguiente'. Finalizando la navegación.")
                break
                
        except Exception as e:
            print(f"Error al buscar o hacer clic en el botón 'Siguiente': {e}")
            print("Intentando un método alternativo para navegar a la siguiente página...")
            
            # Método alternativo: navegar directamente a la URL de la siguiente página
            try:
                next_url = f"{url_base}/page/{pagina_actual + 1}"
                driver.get(next_url)
                # Verificar si la página cargó correctamente (por ejemplo, comprobando el título)
                time.sleep(5)
                if driver.title and "Page not found" not in driver.title:
                    print(f"Navegación alternativa exitosa a la página {pagina_actual + 1}")
                    pagina_actual += 1
                    continue
            except:
                pass
            
            print("Finalizando la navegación por páginas.")
            break
    
    # Mostrar el total de URLs encontradas en todas las páginas
    print(f"\nSe encontraron un total de {len(todas_las_urls)} URLs de logotipos en {pagina_actual} páginas.")
    
    # Crear un DataFrame de Pandas con todas las URLs encontradas
    df = pd.DataFrame({
            'URL del Logotipo': todas_las_urls,
            'Nombre de Marca': [extraer_nombre_marca(url) for url in todas_las_urls]
        })
    
    # Guardar el DataFrame en un archivo de Excel
    try:
        df.to_excel('logotipos_nombres_todas_paginas.xlsx', index=False, engine='openpyxl')
        print("Archivo 'logotipos_nombres_todas_paginas.xlsx' creado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el archivo de Excel: {e}")
    
except Exception as e:
    print(f"Error durante la ejecución: {e}")

finally:
    # Cerrar el navegador al finalizar
    try:
        if 'driver' in locals():
            driver.quit()
            print("Navegador cerrado correctamente.")
    except Exception as e:
        print(f"Error al cerrar el navegador: {e}")