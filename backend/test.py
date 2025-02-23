import streamlit as st 
import os 
from dotenv import load_dotenv
import base64
from openai import OpenAI
from kroger.api_fetch import get_access_token, search_products, get_store_id
from maps_api.stores import get_stores_by_address
from trader_joes.webscrape_joes import get_results

load_dotenv()
key = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o'
client = OpenAI(api_key=key)
client_id = os.getenv("KROGER_CLIENT_ID")
client_secret = os.getenv("KROGER_CLIENT_SECRET")
LOCATOR_URL = "https://alphaapi.brandify.com/rest/locatorsearch"
GRAPHQL_URL = "https://www.traderjoes.com/api/graphql"
APP_KEY = "8BC3433A-60FC-11E3-991D-B2EE0C70A832"

def encode_image(image):
    return base64.b64encode(image.read()).decode('utf-8')

st.title('Image Analyzer')

# User input for recipe
user_message = st.text_input("Enter your recipe (e.g., CAKE):")

# Image upload
image_file = st.file_uploader('Upload an image file', type=['png', 'jpg', 'jpeg'])
if image_file and user_message:
    st.image(image_file, caption='Uploaded image', use_column_width=True)

    base64_image = encode_image(image_file)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a tool which analyzes images of fridges. Given the image, and an input recipe, please tell me which items needed for the recipe are missing."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Return what is missing from the fridge that is needed in {user_message}. Return output as the following: a word list of items, separated by commas. DO NOT provide any other text or output. ONLY a word list."},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    
    st.markdown(response.choices[0].message.content)
    missing_items = response.choices[0].message.content.strip().split(",")
    print(missing_items)
    
    access_token = get_access_token(client_id, client_secret)
    
    # Step 1: Get Access Token
    access_token = get_access_token(client_id, client_secret)

    # Step 2: Get Nearby Stores (Google Maps API)
    address = "3871 Peachtree Rd NE, Brookhaven GA 30319"
    store_list = get_stores_by_address(address)

    # Step 3: Find the Kroger Store from the List
    kroger_store = None
    for store in store_list:
        if store["name"] == "Kroger":
            kroger_store = store
            break

    if kroger_store:
        # Step 4: Retrieve the Kroger Store ID
        kroger_store_id = get_store_id(kroger_store, access_token)
        print("Kroger Store ID:", kroger_store_id)
    else:
        print("No Kroger store found nearby.")
    
    
    st.subheader("Available Items at Kroger:")

    # Loop through each missing item and search in Kroger
    for item in missing_items:
        products = search_products(kroger_store_id, item, access_token)

        if products:
            st.markdown(f"**{item}:**")
            for product in products[:5]:  # Limit results to top 5
                product_name = product.get("description", "No Name")
                price = product["items"][0].get("price", {}).get("regular", "N/A") if product.get("items") else "N/A"
                st.markdown(f"- **{product_name}** - ${price}")
        else:
            st.markdown(f"**{item}:** No products found.")
          
    trader_joes_store = None
    for store in store_list:
        if "Trader Joe's" in store["name"]:
            trader_joes_store = store
            break
    
    if trader_joes_store:
        st.subheader("Available Items at Trader Joe's:")
        for item in missing_items:
            products = get_results(trader_joes_store, item)

            if products:
                st.markdown(f"**{item}:**")
                for product in products[:5]:  # Limit results to top 5
                    product_name = product.get("name")
                    price = product.get("retail_price") if product.get("retail_price") else "N/A"
                    st.markdown(f"- **{product_name}** - ${price}")
            else:
                st.markdown(f"**{item}:** No products found.")
        

                
                
        
        
