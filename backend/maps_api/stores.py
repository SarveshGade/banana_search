import requests
import os
from dotenv import load_dotenv

load_dotenv()

maps_key = os.getenv("maps_key")


def geocode_address(address: str, api_key: str):
    """Convert an address to latitude and longitude using the Geocoding API."""
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(geocode_url, params=params)
    data = response.json()

    import json
    with open("output.txt", 'w') as file:
        json.dump(data, file, indent=4)

    address_components = data["results"][0]["address_components"]
    zipcode = ""
    for element in address_components:
        if element["types"][0] == "postal_code":
            zipcode = element["long_name"]
    
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"], zipcode
    else:
        raise Exception(f"Geocoding API error: {data['status']}")


def search_grocery_stores(lat: float, lng: float, api_key: str, radius: int):
    """
    Search for grocery stores near the provided latitude and longitude using the Places API.
    Filters out results that have 'gas_station' in their types.
    """
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "grocery_or_supermarket",  # Focus on grocery stores
        "key": api_key
    }
    response = requests.get(places_url, params=params)
    data = response.json()
    
    if data["status"] == "OK" or data["status"] == "ZERO_RESULTS":
        results = [
            place for place in data["results"]
            if "gas_station" not in place.get("types", [])
        ]
        # import pprint
        # pprint.pprint(results)
        return results
    else:
        raise Exception("Places API error: " + data["status"])


def search_grocery_keyword(lat: float, lng: float, api_key: str, radius: int):
    """
    Search for locations using a keyword that broadens the search to include stores like Walmart, Costco, and Sam's.
    Filters out results that have 'gas_station' in their types.
    """
    places_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": "grocery walmart costco sam's",
        "key": api_key
    }
    response = requests.get(places_url, params=params)
    data = response.json()
    if data["status"] == "OK" or data["status"] == "ZERO_RESULTS":
        results = [
            place for place in data["results"]
            if "gas_station" not in place.get("types", [])
        ]
        return results
    else:
        raise Exception("Places API error: " + data["status"])


def filter_by_travel_time(origin: str, destinations: list, max_duration_minutes: int):
    """
    Filters destinations to only include those within max_duration_minutes drive time.
    Returns a list of dictionaries containing the store info and its drive time.
    """
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    dest_str = "|".join(
        [f"{store['geometry']['location']['lat']},{store['geometry']['location']['lng']}" for store in destinations]
    )
    params = {
        "origins": origin,
        "destinations": dest_str,
        "mode": "driving",
        "key": maps_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        raise Exception("Distance Matrix API error: " + data["status"])
    
    filtered = []
    for i, element in enumerate(data["rows"][0]["elements"]):
        if element["status"] == "OK":
            duration_minutes = element["duration"]["value"] / 60.0
            if duration_minutes <= max_duration_minutes:
                store_info = destinations[i]
                filtered.append({
                    "name": store_info.get("name"),
                    "lat": store_info.get("geometry").get("location").get("lat"),
                    "lng": store_info.get("geometry").get("location").get("lng"),
                    "vicinity": store_info.get("vicinity"),
                    "drive_time_minutes": round(duration_minutes, 1)
                })
    return filtered


def filter_duplicates_by_brand(stores: list):
    """
    Groups stores by brand and returns only the closest store for each brand.
    Uses the first word in the store's name as a simple brand key.
    """
    filtered = {}
    for store in stores:
        # Using the first word of the store name as the brand key
        brand = store["name"].split()[0]
        if brand in filtered:
            # Keep the store with the shorter drive time
            if store["drive_time_minutes"] < filtered[brand]["drive_time_minutes"]:
                filtered[brand] = store
        else:
            filtered[brand] = store
    return list(filtered.values())

def get_zipcode(address: str):
    API_KEY = maps_key  # Use the API key from the .env file
    lat, lng, zipcode = geocode_address(address, API_KEY)
    return zipcode

def get_stores_by_address(address: str):
    """
    Given an address, this function:
      - Geocodes the address.
      - Searches for nearby grocery stores (using both type and keyword queries).
      - Increases the search radius until at least 10 deduplicated stores are found.
      - Returns a list of store dictionaries.
    """
    API_KEY = maps_key  # Use the API key from the .env file
    lat, lng, zipcode = geocode_address(address, API_KEY)
    origin_str = f"{lat},{lng}"
    
    radius = 5000
    final_stores = []
    
    # Increase or adjust the radius until at least 10 deduplicated stores are found
    while len(final_stores) < 10 and radius < 50000:
        stores = search_grocery_stores(lat, lng, API_KEY, radius)
        stores += search_grocery_keyword(lat, lng, API_KEY, radius)
        
        # If too many results are returned, adjust the radius downward
        if len(stores) > 25:
            radius -= 5000
            stores = search_grocery_stores(lat, lng, API_KEY, radius)
            stores += search_grocery_keyword(lat, lng, API_KEY, radius)
        
            filtered_stores = filter_by_travel_time(origin_str, stores, max_duration_minutes=20)
            final_stores = filter_duplicates_by_brand(filtered_stores)
            break
        
        filtered_stores = filter_by_travel_time(origin_str, stores, max_duration_minutes=20)
        final_stores = filter_duplicates_by_brand(filtered_stores)
        
        if len(final_stores) < 10:
            radius += 5000  # Increase the radius if not enough results
    
    return final_stores


# If running as a script, allow command-line arguments:
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Get nearby grocery stores by address."
    )
    parser.add_argument(
        "--store_address",
        type=str,
        required=True,
        help="The address (or ZIP code) to search near."
    )
    args = parser.parse_args()
    
    stores = get_stores_by_address(args.store_address)
    for store in stores:
        print(f"{store['name']} - {store['vicinity']} (Drive time: {store['drive_time_minutes']} minutes)")