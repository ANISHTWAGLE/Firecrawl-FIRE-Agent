import streamlit as st
from firecrawl import FirecrawlApp
import json
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Amazon Scraper", layout="wide")
st.title("🛍️ Amazon Product Scraper using FIRE-1 Agent")

# Input: API Key & Product Name
api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API Key not found in environment variables. Please set FIRECRAWL_API_KEY.")
product = st.text_input("🔎 Enter the product you want to search on Amazon:")

@st.cache_data(show_spinner="Fetching results...", ttl=600)
def extract_product_data(api_key, product):
    app = FirecrawlApp(api_key=api_key)
    search_url = f"https://www.amazon.com/s?k={product.replace(' ', '+')}"

    prompt = """
    Search for the product and extract around 10 products from the Amazon search results.
    For each product, extract:
    - title
    - price
    - rating
    - number of reviews
    - product URL
    Stop after collecting 10 products.
    """

    schema = {
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "price": {"type": "string"},
                        "rating": {"type": "string"},
                        "reviews": {"type": "string"},
                        "url": {"type": "string"}
                    },
                    "required": ["title", "price", "rating", "reviews", "url"]
                }
            }
        },
        "required": ["products"]
    }

    result = app.extract(
        urls=[search_url],
        prompt=prompt,
        schema=schema,
        agent={
            "model": "FIRE-1"
        }
    )
    return result

if st.button("Scrape Amazon") and api_key and product:
    try:
        data = extract_product_data(api_key, product)
        st.write(data)

    except Exception as e:
        st.error(f"Error: {e}")
