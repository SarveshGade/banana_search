import requests
import argparse
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from maps_api import stores

def get_aldi_stores(zip_code: str, address: str):
    url = "https://api.aldi.us/v1/merchant-search"
    params = {
        "currency": "USD",
        "service_type": "delivery",
        "zip_code": zip_code,
        "address": address
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        # Add additional headers if needed
    }
    
    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def search_aldi_products(store_id: str, keyword: str):
    url = "https://api.aldi.us/v3/product-search"
    params = {
        "currency": "USD",
        "serviceType": "pickup",
        "q": keyword,
        "limit": 30,
        "offset": 0,
        "sort": "relevance",
        "servicePoint": store_id
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://new.aldi.us",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_aldi_products(address, keyword):
    

    zipcode = stores.get_zipcode(address)
    store_list = stores.get_stores_by_address(address)

    aldi_store = None
    for store in store_list:
        if store["name"] == "ALDI":
            aldi_store = store
            break

    if not aldi_store:
        print("No aldi store")
        return

    store_id = None
    try:
        stores_data = get_aldi_stores(zipcode, address)
        data = stores_data.get("data", [])
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
                formatted_address = f"{addr1}, {city}, {region} {zipcode}"
                break

            
    except Exception as e:
        print("Error:", e)
    
    try:
        results = search_aldi_products(store_id, keyword)
        products = results.get("data", [])
        
        if not products:
            print("No products found.")
            return
        
        for product in products:
            name = product.get("name", "Unnamed product")
            price_info = product.get("price", {})
            price_display = price_info.get("amountRelevantDisplay", "N/A")

        return products
            
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    address = "3871 Peachtree Rd NE, Brookhaven, GA 30319"

    keyword = "tortilla"

    get_aldi_products(address, "tortilla")