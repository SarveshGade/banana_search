import requests
import json
import argparse

# --- Configuration ---
LOCATOR_URL = "https://alphaapi.brandify.com/rest/locatorsearch"
GRAPHQL_URL = "https://www.traderjoes.com/api/graphql"
APP_KEY = "8BC3433A-60FC-11E3-991D-B2EE0C70A832"

# --- Helper function for keyword matching ---
def matches_keyword(item_name: str, keyword: str) -> bool:
    """
    Returns True if the keyword appears in the item_name.
    This check is case-insensitive and performs a basic check for singular/plural variations.
    """
    # Normalize both strings to lowercase
    name_lower = item_name.lower()
    keyword_lower = keyword.lower()
    
    # Basic check: does the keyword appear in the name?
    if keyword_lower in name_lower:
        return True
    # Check singular/plural differences: if keyword ends with 's', try without it.
    if keyword_lower.endswith('s') and keyword_lower[:-1] in name_lower:
        return True
    # Or if adding an 's' helps match:
    if (keyword_lower + 's') in name_lower:
        return True
    return False

# --- Function to get store code (clientkey) ---
def get_store_code(store_address: str, search_radius: str = "500", country: str = "US"):
    payload = {
        "request": {
            "appkey": APP_KEY,
            "formdata": {
                "geoip": False,
                "dataview": "store_default",
                "limit": 4,
                "geolocs": {
                    "geoloc": [{
                        "addressline": store_address,
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
        try:
            store = data["response"]["collection"][0]
            store_code = store.get("clientkey")
            if not store_code:
                raise ValueError("Store code not found in response.")
            return store_code
        except (KeyError, IndexError) as e:
            raise Exception("Error parsing store locator response: " + str(e))
    else:
        raise Exception(f"Locator API error: HTTP {response.status_code}")

# --- Function to search products using GraphQL ---
def search_products(store_code: str, search_term: str, page_size: int = 15, current_page: int = 1):
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
        return response.json()
    else:
        raise Exception(f"GraphQL API error: HTTP {response.status_code}")

def get_results(store_address, search_term):
    try:
        store_code = get_store_code(store_address)
        
        products_data = search_products(store_code, search_term)
        items = products_data.get("data", {}).get("products", {}).get("items", [])
        
        # Filter the items so that only those with the keyword in the name are kept.
        filtered_items = [item for item in items if matches_keyword(item.get("name", ""), search_term)]

        return filtered_items
    
    except Exception as e:
        print("An error occurred:", e)

# --- Main execution with argparse ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for a product at a specific Trader Joe's store.")
    parser.add_argument("--store_address", type=str, required=True, help="The store address or ZIP code.")
    parser.add_argument("--search_term", type=str, required=True, help="The product to search for (e.g., eggs).")
    args = parser.parse_args()
    
    get_results(store_address=args.store_address, search_term=args.search_term)