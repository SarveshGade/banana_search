from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
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

app = FastAPI()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
client_id = os.getenv("KROGER_CLIENT_ID")
client_secret = os.getenv("KROGER_CLIENT_SECRET")

# Helper function to encode images
def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

@app.post("/analyze")
async def analyze_image(recipe: str = Form(...), image: UploadFile = File(...), address: str = Form(...)):
    image_bytes = await image.read()
    base64_image = encode_image(image_bytes)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a tool which analyzes images of fridges. Given the image, and an input recipe, please tell me which items needed for the recipe are missing."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Return what is missing from the fridge that is needed in {recipe}. Return output as the following: a word list of items, separated by commas. DO NOT provide any other text or output. ONLY a word list."},
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
        print("KROGER")
        stores_data["Kroger"] = {item: search_products(kroger_store_id, item, access_token) for item in missing_items}

    # Search in Trader Joe's
    trader_joes_store = next((store for store in store_list if "Trader Joe's" in store["name"]), None)
    if trader_joes_store:
        print("TRADER JOES")
        stores_data["Trader Joe's"] = {item: get_results(trader_joes_store, item) for item in missing_items}

    # Search in Aldi
    print ("ALDI")
    stores_data["Aldi"] = {item: get_aldi_products(address, item) for item in missing_items}

    return JSONResponse(content={"missing_items": missing_items, "stores": stores_data})