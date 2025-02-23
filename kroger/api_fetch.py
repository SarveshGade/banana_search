import requests
import base64
import os
import sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from maps_api import stores

from dotenv import load_dotenv

load_dotenv()

def get_access_token(client_id, client_secret):
    """
    Request an OAuth2 access token from Kroger.
    """
    token_url = "https://api.kroger.com/v1/connect/oauth2/token"
    # Prepare the Basic Auth credentials (base64 encoded)
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    print(encoded_credentials)
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"
    }
    
    response = requests.post(token_url, headers=headers, data=data, timeout=10)
    response.raise_for_status()  # raise exception if the call failed
    token = response.json().get("access_token")
    
    if not token:
        raise Exception("Failed to obtain access token.")
    
    return token

def get_store_id(store, token):
    """
    Use the Kroger Location API to search for a store by address.
    Adjust the query parameter based on the API documentation.
    """
    location_url = "https://api.kroger.com/v1/locations"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    store_address = store["vicinity"]
    lat = store["lat"]
    lng = store["lng"]
    
    # The parameter key may vary (e.g., filter.address, filter.postalCode, etc.)
    params = {
        "filter.radiusInMiles": 10,
        "filter.limit": 1,
        "filter.lat.near": lat,
        "filter.lon.near": lng,
    }
    
    response = requests.get(location_url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    if "data" in data and data["data"]:
        # Pick the first matching store
        store = data["data"][0]
        store_id = store.get("locationId")
        print(f"Found store: {store.get('name')} with ID: {store_id}")
        return store_id
    else:
        raise Exception("No store found for the provided address.")

def search_products(store_id, keyword, token):
    """
    Use the Kroger Products API to search for products at a given store.
    """
    products_url = "https://api.kroger.com/v1/products"
    headers = {
        "Authorization": f"bearer {token}",
        "Accept": "application/json",
    }
    params = {
        "filter.locationId": store_id,  # Filter results by store location
        "filter.term": keyword,         # Search term (e.g., "eggs")
        
        "filter.limit": 20              # Limit to 20 results
    }
    
    response = requests.get(products_url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("data", [])

if __name__ == "__main__":
    # Replace with your actual Kroger API client credentials
    client_id = os.getenv("KROGER_CLIENT_ID")
    client_secret = os.getenv("KROGER_CLIENT_SECRET")
    
    # Define the address to search near and the product keyword
    address = "3094 Watson Blvd, Warner Robins, GA"  # Can be a full address or postal code
    search_keyword = "eggs"
    
    store_list = stores.get_stores_by_address(address=address)
    store_address = ""
    for store in store_list:
        if store["name"] == "Kroger":
            kroger = store
            break
    
    try:
        # Step 1: Get the access token
        access_token = get_access_token(client_id, client_secret)
        print("Access token obtained successfully.")
        
        # Step 2: Get a store ID from the location API using the address
        store_id = get_store_id(store, access_token)
                
        # Step 3: Search for products at that store using the products API
        products = search_products(store_id, search_keyword, access_token)
        
        print("\nProducts found:")
<<<<<<< Updated upstream
=======
        # import pprint
        # pprint.pprint(products)
>>>>>>> Stashed changes
        for product in products:
            product_name = product.get("description")
            product_id = product.get("productId")
            # Assume the product's first item holds the pricing info
            price = None
            if product.get("items") and len(product["items"]) > 0:
                price = product["items"][0].get("price", {}).get("regular")
            print(f"Product Name: {product_name}, Price: {price}")
    
    except Exception as e:
        print("Error:", e)
