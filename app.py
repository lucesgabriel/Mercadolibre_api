import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
from groq import Groq
from typing import Generator
import plotly.express as px

# Credenciales de la API de MercadoLibre
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

# Configuración del cliente de Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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

def safe_get(dictionary, key, default="N/A"):
    """
    Obtiene un valor de un diccionario de forma segura, devolviendo un valor por defecto si la clave no existe.
    """
    return dictionary.get(key, default)

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

def safe_percentage(value):
    """
    Convierte un valor a porcentaje de forma segura, manejando posibles errores.
    """
    try:
        return f"{float(value):.2%}"
    except (ValueError, TypeError):
        return str(value)

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
        "Link": safe_get(product, 'permalink')
    }

def generate_summary(data, model_option, max_tokens):
    prompt = f"""
    Analiza los siguientes datos de productos de MercadoLibre y proporciona un resumen conciso:
    
    {json.dumps(data, indent=2)}
    
    El resumen debe incluir:
    1. Una visión general de los productos más populares.
    2. Tendencias de precios.
    3. Patrones en las calificaciones y reseñas de los productos.
    4. Cualquier insight interesante sobre los vendedores.
    
    Por favor, presenta el resumen en un formato fácil de leer con viñetas o párrafos cortos.
    """
    
    chat_completion = client.chat.completions.create(
        model=model_option,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        stream=True
    )
    
    return chat_completion

def generate_summary_stream(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

import plotly.express as px

def main():
    """
    Función principal que configura y ejecuta la aplicación Streamlit.
    """
    st.set_page_config(page_title="MercadoLibre Product Tracker", page_icon="🛒", layout="wide")
    
    st.title("🛒 MercadoLibre Chile Product Tracker")
    
    # Inicializar el estado de la sesión si no existe
    if 'data' not in st.session_state:
        st.session_state.data = []
    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    # Configuración de la barra lateral
    st.sidebar.header("Settings")

    # Opción para ingresar credenciales manualmente
    use_manual_credentials = st.sidebar.checkbox("Enter API credentials manually")

    if use_manual_credentials:
        CLIENT_ID = st.sidebar.text_input("MercadoLibre CLIENT_ID", value=st.secrets.get("CLIENT_ID", ""))
        CLIENT_SECRET = st.sidebar.text_input("MercadoLibre CLIENT_SECRET", value=st.secrets.get("CLIENT_SECRET", ""), type="password")
        GROQ_API_KEY = st.sidebar.text_input("Groq API Key", value=st.secrets.get("GROQ_API_KEY", ""), type="password")
    else:
        CLIENT_ID = st.secrets["CLIENT_ID"]
        CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

    # Configuración del cliente de Groq
    client = Groq(api_key=GROQ_API_KEY)

    # Define model details
    models = {
        "gemma-7b-it": {"name": "Gemma-7b-it", "tokens": 8192, "developer": "Google"},
        "gemma2-9b-it": {"name": "Gemma2-9b-it", "tokens": 8192, "developer": "Google"},
        "llama3-70b-8192": {"name": "LLaMA3-70b-8192", "tokens": 8192, "developer": "Meta"},
        "llama3-8b-8192": {"name": "LLaMA3-8b-8192", "tokens": 8192, "developer": "Meta"},
        "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
    }
    
    # Model selection
    model_option = st.sidebar.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=4  # Default to mixtral
    )

    # Detect model change and clear data if model has changed
    if st.session_state.selected_model != model_option:
        st.session_state.data = []
        st.session_state.selected_model = model_option

    max_tokens_range = models[model_option]["tokens"]

    # Max tokens slider
    max_tokens = st.sidebar.slider(
        "Max Tokens:",
        min_value=512,
        max_value=max_tokens_range,
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens for the model's response. Max for selected model: {max_tokens_range}"
    )

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
                st.session_state.data = []
                for i, product in enumerate(top_products):
                    product_data = fetch_product_data(access_token, product)
                    st.session_state.data.append(product_data)
                    progress_bar.progress((i + 1) / limit)

            st.session_state.category = selected_category
            st.session_state.limit = limit

        except requests.exceptions.HTTPError as http_err:
            st.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            st.error(f"Error connecting to MercadoLibre API: {conn_err}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

    # Mostrar los datos si existen
    if st.session_state.data:
        st.subheader(f"Top {len(st.session_state.data)} products in {st.session_state.category}")
        df = pd.DataFrame(st.session_state.data)
        
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

        # Visualizaciones con Plotly
        st.subheader("Data Visualizations")

        # Gráfico de barras para mostrar los precios de los productos
        fig_prices = px.bar(df, x='Title', y='Price', title='Prices of Top Selling Products')
        st.plotly_chart(fig_prices)

        # Gráfico de dispersión para mostrar la relación entre precio y calificación
        fig_price_rating = px.scatter(df, x='Price', y='Rating', hover_data=['Title'], 
                                      title='Relationship between Price and Rating')
        st.plotly_chart(fig_price_rating)

        # Gráfico circular para mostrar la distribución de condiciones de los productos
        condition_counts = df['Condition'].value_counts()
        fig_conditions = px.pie(values=condition_counts.values, names=condition_counts.index, 
                                title='Distribution of Product Conditions')
        st.plotly_chart(fig_conditions)

        # Botón para descargar los datos como CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f"mercadolibre_{st.session_state.category.lower().replace(' ', '_')}_top_products.csv",
            mime="text/csv",
        )

    # Botón para generar resumen
    if st.button("Generate Summary"):
        if not st.session_state.data:
            st.warning("Please fetch product data first before generating a summary.")
        else:
            st.subheader("Summary of Product Data")
            try:
                with st.spinner("Generating summary..."):
                    summary_completion = generate_summary(st.session_state.data, model_option, max_tokens)
                    summary_container = st.empty()
                    summary = ""
                    for chunk in generate_summary_stream(summary_completion):
                        summary += chunk
                        summary_container.markdown(summary)
                
                # Opción para descargar el resumen
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="mercadolibre_summary.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"An error occurred while generating the summary: {str(e)}")

    # Información en la barra lateral
    st.sidebar.info("This app fetches top-selling products from MercadoLibre Chile based on the selected category. Use the settings above to customize your search.")

# Punto de entrada del script
if __name__ == "__main__":
    main()
