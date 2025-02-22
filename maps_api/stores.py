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
    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
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
    if data["status"] == "OK":
        # Filter out any place that lists 'gas_station' in its types.
        results = [
            place for place in data["results"]
            if "gas_station" not in place.get("types", [])
        ]
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
    if data["status"] == "OK":
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
    # Build a string of destination coordinates separated by '|'
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
    # Process drive time for each destination
    for i, element in enumerate(data["rows"][0]["elements"]):
        if element["status"] == "OK":
            # Convert duration from seconds to minutes
            duration_minutes = element["duration"]["value"] / 60.0
            if duration_minutes <= max_duration_minutes:
                store_info = destinations[i]
                filtered.append({
                    "name": store_info.get("name"),
                    "vicinity": store_info.get("vicinity"),
                    "drive_time_minutes": round(duration_minutes, 1)
                })
    return filtered


def filter_duplicates_by_brand(stores: list):
    """
    Groups stores by brand and returns only the closest store for each brand.
    Uses a list of known brand keywords to match store names.
    """
    
    filtered = {}
    for store in stores:
        
        name = store["name"]
        if name.split()[0] in filtered:
            filtered[name.split()[0]] = store if filtered[name.split()[0]]["drive_time_minutes"] > store["drive_time_minutes"] else filtered[name.split()[0]]
        else:
            filtered[name.split()[0]] = store;

    return filtered.values()


# Example usage:
def get_stores():
    address = "1025 Spring St NW, Atlanta, GA"
    API_KEY = maps_key  # using the API key from the .env file
    
    # Convert the address to coordinates
    lat, lng = geocode_address(address, API_KEY)
    origin_str = f"{lat},{lng}"
    
    radius = 5000
    final_stores = []
    
    # Increase the radius by 5000 until there are at least 10 entries in final_stores
    while len(final_stores) < 10:
        # Gather stores from both search functions using the current radius
        stores = search_grocery_stores(lat, lng, API_KEY, radius)
        stores += search_grocery_keyword(lat, lng, API_KEY, radius)
        
        if len(stores) > 25:
            radius -= 5000
            
            stores = search_grocery_stores(lat, lng, API_KEY, radius)
            stores += search_grocery_keyword(lat, lng, API_KEY, radius)
            
			# Filter stores by drive time
            filtered_stores = filter_by_travel_time(origin_str, stores, max_duration_minutes=20)
			# Remove duplicate brands, keeping only the closest store for each brand
            final_stores = filter_duplicates_by_brand(filtered_stores)
			
            break
            
        # Filter stores by drive time
        filtered_stores = filter_by_travel_time(origin_str, stores, max_duration_minutes=20)
        # Remove duplicate brands, keeping only the closest store for each brand
        final_stores = filter_duplicates_by_brand(filtered_stores)
        
        if len(final_stores) < 10:
            radius += 5000  # Increase the radius if not enough results
    
    # Output the store name, address, and drive time
    for store in final_stores:
        print(f"{store['name']} - {store['vicinity']} (Drive time: {store['drive_time_minutes']} minutes)")
        

get_stores();