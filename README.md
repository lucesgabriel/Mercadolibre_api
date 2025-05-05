# MercadoLibre Chile Product Tracker con Groq AI.

## Descripción
MercadoLibre Chile Product Tracker es una aplicación web avanzada desarrollada con Python y Streamlit que permite a los usuarios rastrear, analizar y generar resúmenes inteligentes de los productos más vendidos en diferentes categorías de MercadoLibre Chile. La aplicación utiliza la API oficial de MercadoLibre para obtener datos en tiempo real sobre productos, visitas, calificaciones y reputación de vendedores, y emplea modelos de lenguaje de Groq AI para generar análisis detallados.

## Características
- Selección de categorías de productos
- Visualización de los productos más vendidos
- Información detallada de cada producto, incluyendo precio, visitas y calificaciones
- Datos sobre la reputación del vendedor
- Interfaz de usuario interactiva con Streamlit
- Generación de resúmenes inteligentes utilizando modelos de lenguaje de Groq AI
- Visualizaciones de datos interactivas con Plotly
- Opción para descargar los datos en formato CSV y los resúmenes generados
- Configuración flexible de credenciales de API

## Requisitos
- Python 3.7+
- pip (gestor de paquetes de Python)
- Cuenta de desarrollador en MercadoLibre (para obtener las credenciales de API)
- Cuenta de Groq AI (para obtener la clave de API)

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/lucesgabriel/Mercadolibre_api.git
   cd Mercadolibre_api
   ```

2. Crea un entorno virtual (opcional, pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configura tus credenciales de API:
   Crea un archivo `.streamlit/secrets.toml` en el directorio del proyecto y añade tus credenciales:
   ```toml
   CLIENT_ID = "tu_client_id_de_mercadolibre"
   CLIENT_SECRET = "tu_client_secret_de_mercadolibre"
   GROQ_API_KEY = "tu_clave_api_de_groq"
   ```

## Uso

1. Ejecuta la aplicación Streamlit:
   ```
   streamlit run app.py
   ```

2. Abre tu navegador y ve a `http://localhost:8501`.

3. Usa la barra lateral para seleccionar una categoría, el número de productos a mostrar, y el modelo de Groq AI a utilizar.

4. Opcionalmente, ingresa manualmente las credenciales de API si lo deseas.

5. Haz clic en "Fetch Products" para obtener y visualizar los datos.

6. Explora los resultados en la tabla interactiva y las visualizaciones generadas.

7. Genera un resumen inteligente de los datos utilizando el modelo de Groq AI seleccionado.

8. Descarga los datos o el resumen generado si lo deseas.

## Estructura del Proyecto
- `app.py`: Script principal de la aplicación Streamlit
- `requirements.txt`: Lista de dependencias del proyecto
- `.streamlit/secrets.toml`: Archivo para almacenar las credenciales de API (no incluido en el repositorio)

## Contribuir
Las contribuciones son bienvenidas. Por favor, sigue estos pasos para contribuir:

1. Haz un Fork del repositorio
2. Crea una nueva rama (`git checkout -b feature/AmazingFeature`)
3. Haz commit de tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Haz Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia
Distribuido bajo la Licencia MIT. Ver `LICENSE` para más información.

## Contacto
Gabriel Luces - lucesgabriel@gmail.com

Enlace del Proyecto: [https://github.com/lucesgabriel/Mercadolibre_api](https://github.com/lucesgabriel/Mercadolibre_api)
