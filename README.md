# Scrapper-dolar-mep
Este codigo implementa un sistema de scraping web concurrente utilizando Python, demostrando la aplicación práctica de conceptos de concurrencia. El sistema obtiene cotizaciones del Dólar MEP de múltiples fuentes web, comparando el rendimiento entre ejecución secuencial y concurrente.

Scraping Concurrente de Cotizaciones Dólar MEP
Este proyecto implementa un sistema de scraping concurrente para obtener cotizaciones del Dólar MEP de diferentes fuentes web. El objetivo principal es demostrar la aplicación práctica de conceptos de concurrencia y paralelismo en Python, comparando el rendimiento entre ejecución secuencial y concurrente.
🚀 Características

Scraping concurrente de múltiples fuentes web (Cronista, IOL, DolarHoy)
Comparación de rendimiento entre ejecución secuencial y concurrente
Generación de reportes detallados con análisis estadístico
Exportación de datos a CSV
Métricas de rendimiento y tiempo de ejecución

📋 Requisitos
python >= 3.8
pandas
selenium
beautifulsoup4
webdriver_manager
tabulate
requests
🔧 Instalación

Clonar el repositorio:

git clone https://github.com/luigiydm/Scrapper-dolar-mep.git
cd scraping-dolar-mep

Instalar dependencias:

pip install -r requirements.txt
💻 Uso
Para ejecutar el programa:
python main.py
El programa generará:

Un archivo CSV con las cotizaciones obtenidas
Un archivo CSV con métricas de rendimiento
Un reporte detallado en formato TXT

📊 Estructura del Proyecto
Copyscraping-dolar-mep/
│
├── main.py                 # Archivo principal del programa
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
└── output/                # Directorio para archivos generados
    ├── dolar_mep_*.csv    # Datos de cotizaciones
    ├── performance_*.csv  # Métricas de rendimiento
    └── reporte_*.txt      # Reportes detallados
🛠️ Tecnologías Utilizadas

Python: Lenguaje de programación principal
concurrent.futures: Módulo para implementar concurrencia
Selenium: Para web scraping dinámico
BeautifulSoup: Para parsing de HTML
Pandas: Para manejo y exportación de datos

📈 Rendimiento
El programa compara automáticamente los tiempos de ejecución entre:

Ejecución secuencial (un sitio a la vez)
Ejecución concurrente (múltiples sitios en paralelo)

Los resultados de rendimiento se guardan en un archivo CSV para análisis posterior.
👥 Contribuir
Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de crear un pull request.
📄 Licencia
Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE.md para detalles.
