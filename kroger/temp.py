import os
import requests
import json

from dotenv import load_dotenv

load_dotenv()

# Set your Kroger API credentials
# It is recommended to store these as environment variables.
KROGER_CLIENT_ID = os.getenv("KROGER_CLIENT_ID")
KROGER_CLIENT_SECRET = os.getenv("KROGER_CLIENT_SECRET")
# Endpoint to obtain OAuth2 access token
TOKEN_URL = "https://api.kroger.com/v1/connect/oauth2/token"

# Endpoint for product search (this example uses the compact product endpoint)
PRODUCT_SEARCH_URL = "https://api.kroger.com/v1/products"

def get_access_token():
    """
    Uses client credentials to get an access token from the Kroger API.
    """
    # Kroger requires basic authentication with the client_id and client_secret
    auth = (KROGER_CLIENT_ID, KROGER_CLIENT_SECRET)
    
    # Request parameters (adjust scope as needed)
    data = {
        "grant_type": "client_credentials",
        "scope": "product.compact"  # or another scope depending on your needs
    }
    
    response = requests.post(TOKEN_URL, auth=auth, data=data)
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get("access_token")
    else:
        raise Exception(f"Error obtaining access token: {response.status_code} {response.text}")

def search_products(keyword, access_token):
    """
    Searches for products with the given keyword using Kroger's product search endpoint.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    # Set up the query parameters.
    # The API supports filtering with 'filter.term'. Adjust parameters as needed.
    params = {
        "filter.term": keyword,
        "filter.limit": 20  # limit the number of results, adjust as needed
    }
    
    response = requests.get(PRODUCT_SEARCH_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Product search error: {response.status_code} {response.text}")

def main():
    keyword = "eggs"
    try:
        access_token = get_access_token()
        print("Access token obtained successfully.")
        products = search_products(keyword, access_token)
        # Print the JSON response nicely formatted
        print("Product search results for keyword 'eggs':")
        print(json.dumps(products, indent=2))
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    main()