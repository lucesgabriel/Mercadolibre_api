import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json  # Asegúrate de importar json al principio del archivo

# Credenciales de la API de MercadoLibre
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

# Diccionario ampliado de categorías
CATEGORIES = {
    "Technology": "MLC1648",
    "Home & Appliances": "MLC1574",
    "Sports & Fitness": "MLC1276",
    "Beauty & Personal Care": "MLC1246",
    "Toys & Games": "MLC1132",
    "Books, Movies & Music": "MLC3025",
    "Vehicles": "MLC1743",
    "Fashion": "MLC1430",
    "Electronics": "MLC1000",
    "Computers": "MLC1648",
    "Cellphones & Smartphones": "MLC1051",
    "Cameras & Photography": "MLC1039",
    "Video Games & Consoles": "MLC1144",
    "Home & Garden": "MLC1574",
    "Tools & Construction": "MLC1500",
    "Industrial Equipment": "MLC1499",
    "Services": "MLC1540",
    "Real Estate": "MLC1459",
    "Food & Drinks": "MLC1403",
    "Office Supplies": "MLC1499",
    "Health & Medical Equipment": "MLC1246"
}

# Función para obtener el token de acceso
@st.cache_data(ttl=3600)
def get_access_token():
    """
    Obtiene el token de acceso de la API de MercadoLibre.
    Este token es necesario para hacer todas las demás llamadas a la API.
    """
    url = "https://api.mercadolibre.com/oauth/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

# Función para obtener los productos más vendidos de una categoría
def get_top_products(access_token, category_id, limit=20):
    """
    Obtiene los productos más vendidos de una categoría específica.
    """
    url = "https://api.mercadolibre.com/sites/MLC/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "category": category_id,
        "sort": "sold_quantity_desc",
        "limit": limit
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['results']

# Función para obtener las visitas de un producto
def get_item_visits(access_token, item_id):
    """
    Obtiene el número de visitas de un producto en los últimos 30 días.
    """
    end_date = datetime.now()
    url = f"https://api.mercadolibre.com/items/{item_id}/visits/time_window"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "last": 30,
        "unit": "day",
        "ending": end_date.strftime("%Y-%m-%d")
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get('total_visits', 'N/A')

# Función para obtener la calificación de un producto
def get_item_rating(access_token, item_id):
    """
    Obtiene la calificación promedio, las reseñas y la distribución de calificaciones de un producto.
    """
    url = f"https://api.mercadolibre.com/reviews/item/{item_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return (
        data.get('rating_average', 'N/A'),
        data.get('reviews', []),
        data.get('rating_levels', {})
    )

# Función para obtener la reputación del vendedor
def get_seller_reputation(access_token, seller_id):
    """
    Obtiene la información de reputación de un vendedor específico.
    """
    url = f"https://api.mercadolibre.com/users/{seller_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        reputation = data.get('seller_reputation', {})
        transactions = reputation.get('transactions', {})
        
        return {
            "level_id": reputation.get('level_id', 'N/A'),
            "power_seller_status": reputation.get('power_seller_status', 'N/A'),
            "transactions_total": transactions.get('total', 'N/A'),
            "transactions_completed": transactions.get('completed', 'N/A'),
            "transactions_canceled": transactions.get('canceled', 'N/A'),
            "positive_ratings": 'N/A',
            "neutral_ratings": 'N/A',
            "negative_ratings": 'N/A',
        }
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la reputación del vendedor {seller_id}: {e}")
        return {}

# Función auxiliar para obtener valores de un diccionario de forma segura
def safe_get(dictionary, key, default="N/A"):
    """
    Obtiene un valor de un diccionario de forma segura, devolviendo un valor por defecto si la clave no existe.
    """
    return dictionary.get(key, default)

# Función para formatear los niveles de calificación
def format_rating_levels(rating_levels):
    """
    Formatea los niveles de calificación en una cadena legible.
    """
    return (
        f"⭐: {rating_levels.get('one_star', 0)} | "
        f"⭐⭐: {rating_levels.get('two_star', 0)} | "
        f"⭐⭐⭐: {rating_levels.get('three_star', 0)} | "
        f"⭐⭐⭐⭐: {rating_levels.get('four_star', 0)} | "
        f"⭐⭐⭐⭐⭐: {rating_levels.get('five_star', 0)}"
    )

# Función para formatear porcentajes de forma segura
def safe_percentage(value):
    """
    Convierte un valor a porcentaje de forma segura, manejando posibles errores.
    """
    try:
        return f"{float(value):.2%}"
    except (ValueError, TypeError):
        return str(value)

# Función para obtener todos los datos de un producto
def fetch_product_data(access_token, product):
    """
    Obtiene todos los datos relevantes de un producto, incluyendo visitas, calificaciones y reputación del vendedor.
    """
    item_id = product['id']
    visits = get_item_visits(access_token, item_id)
    rating, reviews, rating_levels = get_item_rating(access_token, item_id)
    seller_reputation = get_seller_reputation(access_token, product['seller']['id'])
    
    return {
        "Title": safe_get(product, 'title'),
        "Price": f"${safe_get(product, 'price', 0):,.0f}",
        "Available Quantity": safe_get(product, 'available_quantity'),
        "Condition": safe_get(product, 'condition').capitalize(),
        "Visits (Last 30 days)": visits,
        "Rating": rating,
        "Number of Reviews": len(reviews),
        "Rating Distribution": format_rating_levels(rating_levels),
        "Seller Level": seller_reputation.get('level_id', 'N/A'),
        "Power Seller Status": seller_reputation.get('power_seller_status', 'N/A'),
        "Total Transactions": seller_reputation.get('transactions_total', 'N/A'),
        "Positive Ratings": seller_reputation.get('positive_ratings', 'N/A'),
        "Neutral Ratings": seller_reputation.get('neutral_ratings', 'N/A'),
        "Negative Ratings": seller_reputation.get('negative_ratings', 'N/A'),
        "Link": safe_get(product, 'permalink')
    }

# Función principal que ejecuta la aplicación Streamlit
def main():
    """
    Función principal que configura y ejecuta la aplicación Streamlit.
    """
    st.set_page_config(page_title="MercadoLibre Product Tracker", page_icon="🛒", layout="wide")
    
    st.title("🛒 MercadoLibre Chile Product Tracker")
    
    # Configuración de la barra lateral
    st.sidebar.header("Settings")
    selected_category = st.sidebar.selectbox(
        "Choose a category:",
        list(CATEGORIES.keys())
    )
    
    limit = st.sidebar.slider("Number of products to fetch", 5, 50, 20)

    # Botón para iniciar la búsqueda de productos
    if st.sidebar.button("Fetch Products"):
        try:
            with st.spinner('Fetching products, visit data, ratings, and seller reputation...'):
                access_token = get_access_token()
                category_id = CATEGORIES[selected_category]
                top_products = get_top_products(access_token, category_id, limit)

                progress_bar = st.progress(0)
                data = []
                for i, product in enumerate(top_products):
                    product_data = fetch_product_data(access_token, product)
                    # Eliminar los campos de calificaciones que siempre son N/A
                    product_data.pop('Positive Ratings', None)
                    product_data.pop('Neutral Ratings', None)
                    product_data.pop('Negative Ratings', None)
                    data.append(product_data)
                    progress_bar.progress((i + 1) / limit)

            st.subheader(f"Top {limit} products in {selected_category}")

            df = pd.DataFrame(data)
            
            # Configurar y mostrar el DataFrame
            st.dataframe(
                df,
                column_config={
                    "Link": st.column_config.LinkColumn("Product Link"),
                    "Rating Distribution": st.column_config.Column(
                        "Rating Distribution",
                        help="Distribution of ratings from 1 to 5 stars",
                        width="medium",
                    ),
                    "Seller Level": st.column_config.Column(
                        "Seller Level",
                        help="Seller's reputation level",
                        width="small",
                    ),
                    "Power Seller Status": st.column_config.Column(
                        "Power Seller Status",
                        help="Seller's power seller status",
                        width="small",
                    ),
                },
                hide_index=True
            )

            # Botón para descargar los datos como CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f"mercadolibre_{selected_category.lower().replace(' ', '_')}_top_products.csv",
                mime="text/csv",
            )

        # Manejo de errores
        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"Error connecting to MercadoLibre API: {conn_err}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

    # Información en la barra lateral
    st.sidebar.info("This app fetches top-selling products from MercadoLibre Chile based on the selected category. Use the settings above to customize your search.")

# Punto de entrada del script
if __name__ == "__main__":
    main()