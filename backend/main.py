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
from maps_api.stores import get_stores_by_address, get_zipcode
from trader_joes.webscrape_joes import get_results
from aldi.webscrape_aldi import get_aldi_products, get_aldi_stores

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
async def analyze_image(dish: str = Form(...), image: UploadFile = File(...)):
    image_bytes = await image.read()
    base64_image = encode_image(image_bytes)
    recipe = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tool which given a dish to make, generates a detailed recipe, with an ingredient list followed by steps to make the dish."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Generate Recipe for {dish}. Return output as an array with an ingredient list, followed by recipe steps."},
            ]}
        ],
        temperature=0.0,
    )
    recipe = recipe.choices[0].message.content.strip()
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
    return JSONResponse(content={"recipe": recipe, "missing_items": missing_items})
    
    
    
    
@app.post("/groceries")
async def api_calls(ingredient_list: str = Form(...), address: str = Form(...)):
    access_token = get_access_token(client_id, client_secret)
    address = address
    store_list = get_stores_by_address(address)
    
    stores_data = {}
    kroger_store = next((store for store in store_list if "Kroger" in store["name"]), None)
    if kroger_store:
        kroger_store_id = get_store_id(kroger_store, access_token)
        kroger_address = kroger_store['vicinity']
        drive_time = kroger_store['drive_time_minutes']

        stores_data["Kroger"] = {"address": kroger_address, "drive_time_minutes": drive_time, "ingredients": {}}

        for item in ingredient_list:
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
            stores_data["Kroger"]["ingredients"][item] = sorted(temp, key = lambda x: x['price'])[0]

    

    # Search in Trader Joe's
    trader_joes_store = next((store for store in store_list if "Trader Joe's" in store["name"]), None)
    if trader_joes_store:
        # For each missing ingredient (search term)
        joes_address = trader_joes_store['vicinity']
        drive_time = trader_joes_store['drive_time_minutes']

        stores_data["Trader Joe's"] = {"address": joes_address, "drive_time_minutes": drive_time, "ingredients": {}}
        for item in ingredient_list:
            
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
            stores_data["Trader Joe's"]["ingredients"][item] = sorted(product_list, key = lambda x: x['retail_price'])[0]

    zipcode = get_zipcode(address)

    aldi_store = None
    for store in store_list:
        if store["name"] == "ALDI":
            aldi_store = store
            break

    if not aldi_store:
        print("No aldi store")
        return
    
    aldi_address = aldi_store['vicinity']
    drive_time = aldi_store['drive_time_minutes']
    
    store_id = None
    try:
        aldi_stores = get_aldi_stores(zipcode, address)
        data = aldi_stores.get("data", [])
        if not data:
            print("No stores found.")
            exit(0)
            
        for store in data:
            store_id = store.get("id", "Unknown ID")
            attributes = store.get("attributes", {})
            address_obj = attributes.get("address", {})

            if round(float(address_obj.get("latitude")), 2) == round(float(aldi_store["lat"]), 2) and round(float(address_obj.get("latitude")), 2) == round(float(aldi_store["lat"]), 2):
                addr1 = address_obj.get("address1", "")
                city = address_obj.get("city", "")
                region = address_obj.get("regionName", "")
                zipcode = address_obj.get("zipCode", "")
                formatted_address = f"{addr1}, {city}, {region}"
                break

            
    except Exception as e:
        print("Error:", e)
        
    # Search in Aldi
    if aldi_store:
        stores_data["Aldi"] = {"address": aldi_address, "drive_time_minutes": drive_time, "ingredients": {}}
        for item in ingredient_list:  # For each missing ingredient
            # Retrieve Aldi products for the given address and search term
            products = get_aldi_products(store_id, item)
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
            stores_data["Aldi"]["ingredients"][item] = sorted(product_list, key = lambda x: x['retail_price'])[0]  # ADDED: Assign product list for this missing item

    # import json
    # with open("output.txt", "w") as file:
    #     json.dump(stores_data, file, indent=4)


    return JSONResponse(content={"ingredient_list": ingredient_list, "stores": stores_data})


# if __name__ == "__main__":
    
#     api_calls(["carrots", "tortilla", "eggs", "ham", "cheese"], "3871 Peachtree Rd NE, Brookhaven, GA 30319")