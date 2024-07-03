# MercadoLibre Chile Product Tracker

## Descripción
MercadoLibre Chile Product Tracker es una aplicación web desarrollada con Python y Streamlit que permite a los usuarios rastrear y analizar los productos más vendidos en diferentes categorías de MercadoLibre Chile. La aplicación utiliza la API oficial de MercadoLibre para obtener datos en tiempo real sobre productos, visitas, calificaciones y reputación de vendedores.

## Características
- Selección de categorías de productos
- Visualización de los productos más vendidos
- Información detallada de cada producto, incluyendo precio, visitas y calificaciones
- Datos sobre la reputación del vendedor
- Interfaz de usuario interactiva con Streamlit
- Opción para descargar los datos en formato CSV

## Requisitos
- Python 3.7+
- pip (gestor de paquetes de Python)
- Cuenta de desarrollador en MercadoLibre (para obtener las credenciales de API)

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu_usuario/mercadolibre-product-tracker.git
   cd mercadolibre-product-tracker
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

4. Configura tus credenciales de API de MercadoLibre:
   Crea un archivo `.streamlit/secrets.toml` en el directorio del proyecto y añade tus credenciales:
   ```toml
   CLIENT_ID = "tu_client_id"
   CLIENT_SECRET = "tu_client_secret"
   ```

## Uso

1. Ejecuta la aplicación Streamlit:
   ```
   streamlit run app.py
   ```

2. Abre tu navegador y ve a `http://localhost:8501`.

3. Usa la barra lateral para seleccionar una categoría y el número de productos a mostrar.

4. Haz clic en "Fetch Products" para obtener y visualizar los datos.

5. Explora los resultados en la tabla interactiva y descarga los datos si lo deseas.

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
Gabriel Luces - [lucesgabriel@gmail.com](mailto:tu@email.com)

Enlace del Proyecto: [https://github.com/lucesgabriel/Mercadolibre_api.git]
