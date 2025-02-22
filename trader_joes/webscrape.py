import requests
import json

# --- Configuration ---
# These endpoints and payload structures are based on the provided cURL examples.
LOCATOR_URL = "https://alphaapi.brandify.com/rest/locatorsearch"
GRAPHQL_URL = "https://www.traderjoes.com/api/graphql"

# For the locator search, we use a fixed appkey from the example.
APP_KEY = "8BC3433A-60FC-11E3-991D-B2EE0C70A832"

# --- Function to get store code (clientkey) ---
def get_store_code(store_address: str, search_radius: str = "500", country: str = "US"):
    """
    Send a POST request to the Trader Joe's locator API (Brandify) to search for a store.
    Returns the store code (clientkey) of the first matching store.
    """
    payload = {
        "request": {
            "appkey": APP_KEY,
            "formdata": {
                "geoip": False,
                "dataview": "store_default",
                "limit": 4,
                "geolocs": {
                    "geoloc": [{
                        "addressline": store_address,  # can be a full address or ZIP code
                        "country": country,
                        "latitude": "",
                        "longitude": ""
                    }]
                },
                "searchradius": search_radius,
                "where": {
                    "warehouse": {"distinctfrom": "1"}
                },
                "false": "0"
            }
        }
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.traderjoes.com",
        "referer": "https://www.traderjoes.com/"
    }
    response = requests.post(LOCATOR_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # Debug: print(data)
        # Here, adjust according to the actual response structure.
        # For example, if the first store is located at data["response"]["results"][0],
        # and its clientkey is stored under the key "clientkey":
        try:
            print(data["response"]["collection"][0]["clientkey"])
            store = data["response"]["collection"][0]
            # The store identifier might be under "clientkey" or another similar key.
            store_code = store.get("clientkey")  # Adjust this if the key is different.
            if not store_code:
                raise ValueError("Store code not found in response.")
            return store_code
        except (KeyError, IndexError) as e:
            raise Exception("Error parsing store locator response: " + str(e))
    else:
        raise Exception(f"Locator API error: HTTP {response.status_code}")

# --- Function to search products using GraphQL ---
def search_products(store_code: str, search_term: str, page_size: int = 15, current_page: int = 1):
    """
    Use the Trader Joe's GraphQL API to search for products at a specific store.
    The store_code is used as the "storeCode" in the query variables.
    """
    # Construct the GraphQL payload with variables.
    payload = {
        "operationName": "SearchProducts",
        "variables": {
            "storeCode": store_code,
            "availability": "1",
            "published": "1",
            "search": search_term,
            "currentPage": current_page,
            "pageSize": page_size
        },
        "query": (
            "query SearchProducts($search: String, $pageSize: Int, $currentPage: Int, "
            "$storeCode: String = \"" + store_code + "\", $availability: String = \"1\", $published: String = \"1\") {"
            "  products("
            "    search: $search "
            "    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}} "
            "    pageSize: $pageSize "
            "    currentPage: $currentPage"
            "  ) {"
            "    items {"
            "      name "
            "      sku "
            "      retail_price "
            "    } "
            "    total_count "
            "    page_info {"
            "      current_page "
            "      page_size "
            "      total_pages "
            "    }"
            "  }"
            "}"
        )
    }
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://www.traderjoes.com",
        "referer": "https://www.traderjoes.com/home/search?q=" + search_term + "&global=yes",
        "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    response = requests.post(GRAPHQL_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"GraphQL API error: HTTP {response.status_code}")

# --- Main script execution ---
if __name__ == "__main__":
    # Input: store's address (or ZIP code) and search term.
    store_address = "931 Monroe Drive Northeast, Atlanta"
    search_term = "eggs"
    
    try:
        # Step 1: Locate the store and obtain its code
        store_code = get_store_code(store_address)
        print(f"Found store code: {store_code}")
        
        # Step 2: Search for the product using the store code
        products_data = search_products(store_code, search_term)
        
        # Print the found products (adjust the parsing as needed)
        items = products_data.get("data", {}).get("products", {}).get("items", [])
        if items:
            print(f"Products found for '{search_term}' at store {store_code}:")
            for item in items:
                name = item.get("name")
                sku = item.get("sku")
                price = item.get("retail_price")
                print(f"Name: {name} | SKU: {sku} | Price: {price}")
        else:
            print(f"No products found for '{search_term}' at store {store_code}.")
    
    except Exception as e:
        print("An error occurred:", e)