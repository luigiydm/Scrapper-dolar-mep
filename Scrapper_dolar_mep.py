import concurrent.futures
import pandas as pd
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import statistics
import os
from selenium.common.exceptions import TimeoutException, WebDriverException

def setup_driver(page_load_timeout=30, script_timeout=30):
    """Configura y retorna el driver de Selenium con timeouts personalizados"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-notifications')
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(page_load_timeout)
    driver.set_script_timeout(script_timeout)
    return driver

def retry_scraper(func, max_retries=3, delay=5):
    """Decorador para reintentar el scraping en caso de error"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Error final en {func.__name__} después de {max_retries} intentos: {str(e)}")
                    return None
                print(f"Intento {attempt + 1} fallido en {func.__name__}: {str(e)}")
                time.sleep(delay)
        return None
    return wrapper

@retry_scraper
def scrape_cronista():
    """Scraping de la cotización del dólar MEP en Cronista"""
    start_time = time.time()
    driver = None
    try:
        driver = setup_driver()
        url = 'https://www.cronista.com/MercadosOnline/dolar.html'
        
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul#market-scrll-1')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        dolar_items = soup.select('ul#market-scrll-1 li')
        
        for item in dolar_items:
            nombre = item.find('span', class_='name')
            if nombre and 'MEP' in nombre.text.strip():
                valor = item.find('span', class_='value')
                if valor:
                    valor_text = valor.text.strip()
                    valor = float(valor_text.replace('$', '').replace('.', '').replace(',', '.'))
                    current_time = datetime.now().strftime("%d/%m/%y %H:%M")
                    execution_time = round(time.time() - start_time, 2)
                    return {
                        'web': 'Cronista',
                        'timestamp': current_time,
                        'valor': round(valor, 2),
                        'tiempo_ejecucion': execution_time
                    }
        return None
    except TimeoutException:
        print("Timeout en Cronista - la página tardó demasiado en cargar")
        return None
    except WebDriverException as e:
        print(f"Error del WebDriver en Cronista: {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado en Cronista: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@retry_scraper
def scrape_iol():
    """Scraping de la cotización del dólar MEP en IOL"""
    start_time = time.time()
    driver = None
    try:
        driver = setup_driver()
        url = 'https://iol.invertironline.com/mercado/cotizaciones/argentina/monedas'
        
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'tr')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all('tr')
        
        for row in rows:
            strong = row.find('strong')
            if strong and 'MEP' in strong.text:
                tds = row.find_all('td', class_='tar')
                if len(tds) >= 2:
                    valor_text = tds[1].text.strip()
                    valor = float(valor_text.replace('.', '').replace(',', '.'))
                    current_time = datetime.now().strftime("%d/%m/%y %H:%M")
                    execution_time = round(time.time() - start_time, 2)
                    return {
                        'web': 'IOL',
                        'timestamp': current_time,
                        'valor': round(valor, 2),
                        'tiempo_ejecucion': execution_time
                    }
        return None
    except TimeoutException:
        print("Timeout en IOL - la página tardó demasiado en cargar")
        return None
    except WebDriverException as e:
        print(f"Error del WebDriver en IOL: {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado en IOL: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

@retry_scraper
def scrape_dolarhoy():
    """Scraping de la cotización del dólar MEP en DolarHoy"""
    start_time = time.time()
    driver = None
    try:
        driver = setup_driver(page_load_timeout=200)
        url = 'https://dolarhoy.com/cotizacion-dolar-mep'
        
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'value')))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        values = soup.find_all('div', class_='value')
        
        if len(values) >= 2:
            valor_text = values[1].text.strip()
            valor = float(valor_text.replace('$', '').replace('.', '').replace(',', '.'))
            current_time = datetime.now().strftime("%d/%m/%y %H:%M")
            execution_time = round(time.time() - start_time, 2)
            return {
                'web': 'DolarHoy',
                'timestamp': current_time,
                'valor': round(valor, 2),
                'tiempo_ejecucion': execution_time
            }
        return None
    except TimeoutException:
        print("Timeout en DolarHoy - la página tardó demasiado en cargar")
        return None
    except WebDriverException as e:
        print(f"Error del WebDriver en DolarHoy: {str(e)}")
        return None
    except Exception as e:
        print(f"Error inesperado en DolarHoy: {str(e)}")
        return None
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def generate_report(results, tiempo_total):
    """Genera un reporte detallado de los resultados"""
    report = []
    report.append("\n" + "="*50)
    report.append("INFORME DE COTIZACIÓN DÓLAR MEP")
    report.append("="*50)
    
    report.append(f"\nFecha y hora del informe: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    if results:
        table_data = [[r['web'], r['timestamp'], f"${r['valor']:.2f}", f"{r['tiempo_ejecucion']}s"] 
                     for r in results]
        headers = ['Fuente', 'Timestamp', 'Valor MEP', 'Tiempo Ejec.']
        table = tabulate(table_data, headers=headers, tablefmt='grid')
        report.append("\nResultados por fuente:")
        report.append(table)
        
        valores = [r['valor'] for r in results]
        report.append("\nAnálisis estadístico:")
        report.append(f"Valor promedio: ${statistics.mean(valores):.2f}")
        report.append(f"Valor máximo: ${max(valores):.2f}")
        report.append(f"Valor mínimo: ${min(valores):.2f}")
        if len(valores) > 1:
            report.append(f"Desviación estándar: ${statistics.stdev(valores):.2f}")
        
        max_diff = max(valores) - min(valores)
        report.append(f"Spread máximo entre fuentes: ${max_diff:.2f}")
    
    report.append("\nMétricas de rendimiento:")
    report.append(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    if results:
        report.append(f"Tiempo promedio por fuente: {statistics.mean([r['tiempo_ejecucion'] for r in results]):.2f} segundos")
    
    os.makedirs('output', exist_ok=True)
    
    report_filename = os.path.join('output', f'reporte_dolar_mep_{datetime.now().strftime("%Y%m%d_%H%M")}.txt')
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    return "\n".join(report), report_filename

def main():
    """Función principal para ejecutar el scraping y generar reportes"""
    scraping_functions = [scrape_cronista, scrape_iol, scrape_dolarhoy]

    print("\nEjecución secuencial:")
    start_time = time.time()
    sequential_results = [func() for func in scraping_functions]
    sequential_results = [r for r in sequential_results if r]
    sequential_time = time.time() - start_time

    print("\nEjecución concurrente:")
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        concurrent_results = list(executor.map(lambda func: func(), scraping_functions))
    concurrent_results = [r for r in concurrent_results if r]
    concurrent_time = time.time() - start_time

    # Generar reporte para los resultados secuenciales
    if sequential_results:
        sequential_report, sequential_report_filename = generate_report(sequential_results, sequential_time)
        print(f"\nReporte secuencial guardado en {sequential_report_filename}")
        print(sequential_report)

    # Generar reporte para los resultados concurrentes
    if concurrent_results:
        concurrent_report, concurrent_report_filename = generate_report(concurrent_results, concurrent_time)
        print(f"\nReporte concurrente guardado en {concurrent_report_filename}")
        print(concurrent_report)

    # Comparación de rendimiento
    print("\nComparación de rendimiento:")
    print(f"Tiempo de ejecución secuencial: {sequential_time:.2f} segundos")
    print(f"Tiempo de ejecución concurrente: {concurrent_time:.2f} segundos")

if __name__ == "__main__":
    main()
