from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import base64
import io
from PIL import Image
from openai import OpenAI
from kroger.api_fetch import get_access_token, search_products, get_store_id
from maps_api.stores import get_stores_by_address
from trader_joes.webscrape_joes import get_results
from aldi.webscrape_aldi import get_aldi_products

load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client_id = os.getenv("KROGER_CLIENT_ID")
client_secret = os.getenv("KROGER_CLIENT_SECRET")

# Helper function to encode images
def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

@app.post("/analyze")
async def analyze_image(dish: str = Form(...), image: UploadFile = File(...), address: str = Form(...)):
    image_bytes = await image.read()
    base64_image = encode_image(image_bytes)
    recipe = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tool which given a dish to make, generates a detailed recipe, with an ingredient list followed by steps to make the dish."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Return output as a JSON with an ingredient list, followed by recipe steps."},
            ]}
        ],
        temperature=0.0,
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tool which analyzes images of fridges. Given the image, and an input recipe, please tell me which items needed for the recipe are missing."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Return what is missing from the fridge that is needed in the below recipe. Return output as the following: a word list of items, separated by commas. DO NOT provide any other text or output. ONLY a word list. {recipe}"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        temperature=0.0,
    )
    missing_items = response.choices[0].message.content.strip().split(",")
    access_token = get_access_token(client_id, client_secret)
    address = address
    store_list = get_stores_by_address(address)
    
    stores_data = {}
    kroger_store = next((store for store in store_list if "Kroger" in store["name"]), None)
    if kroger_store:
        kroger_store_id = get_store_id(kroger_store, access_token)
        
        stores_data["Kroger"] = {}
        for item in missing_items:
            # Get the list of products matching this missing item from Kroger
            products = search_products(kroger_store_id, item, access_token)
            temp = []  # We'll store product details in a list
            for product in products[:5]:
                # Extract product name (assuming it's under the key "description")
                product_name = product.get("description")
                price = None
                # Extract the price if available
                if product.get("items") and len(product["items"]) > 0:
                    price = product["items"][0].get("price", {}).get("regular")
                # Append a dictionary with the product's name and price
                temp.append({
                    "name": product_name,
                    "price": price
                })
            # Map the missing item to its list of products in the Kroger data
            stores_data["Kroger"][item] = temp

    

    # Search in Trader Joe's
    trader_joes_store = next((store for store in store_list if "Trader Joe's" in store["name"]), None)
    if trader_joes_store:
        # For each missing ingredient (search term)
        stores_data["Trader Joe's"] = {}
        for item in missing_items:
            
            # Get products from Trader Joe's using your custom function.
            # get_results is assumed to return a list of products for the given store and search term.
            products = get_results(trader_joes_store, item)
            
            product_list = []  # Will store the processed product info for this missing item
            for product in products[:5]:
                # Extract product details. Adjust key names if needed.
                product_name = product.get("name")  # e.g., "TORTILLAS SONORA STYLE FLOUR"
                # Depending on the API, the price might be nested in a dictionary.
                # Here we try to extract "retail_price" or fallback to another key.
                retail_price = product.get("retail_price") or product.get("price", {}).get("amountRelevantDisplay")
                
                # Append the product details to the list
                product_list.append({
                    "name": product_name,
                    "retail_price": retail_price
                })
            
            # Map the missing item to its product list in the Trader Joe's section
            stores_data["Trader Joe's"][item] = product_list

    # Search in Aldi
    stores_data["Aldi"] = {}  # Initialize Aldi key in our results
    for item in missing_items:  # For each missing ingredient
        # Retrieve Aldi products for the given address and search term
        products = get_aldi_products(address, item)
        if not products:
            continue
        product_list = []  # Initialize a list to hold product details for this item
        for product in products[:5]:  # Limit to first 5 products for brevity
            name = product.get("name")  # Extract product name
            retail_price = product.get("price", {}).get("amountRelevantDisplay")  # Extract price display
            product_list.append({
                "name": name,
                "retail_price": retail_price
            })
        # Map the missing item to its list of products under Aldi
        stores_data["Aldi"][item] = product_list  # ADDED: Assign product list for this missing item



    return JSONResponse(content={"recipe":recipe, "missing_items": missing_items, "stores": stores_data})