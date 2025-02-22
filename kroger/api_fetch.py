import requests
import base64

# Replace these with your actual client credentials from Kroger
client_id = "bananasearch-2432612430342443456151656b6b387835666733612f48794e33516a656e6d58344b4f7a54626f593057446a654c4a385431683861317a4248576e32447431493318118543"
client_secret = "jhAz1Zwx63-iVvrVMGmJTKnvZid65UtD1yryiXKw"

# Encode the client credentials for the Basic Auth header
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

token_url = "https://api.kroger.com/v1/connect/oauth2/token"
headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "client_credentials",
    "scope": "product.compact location.compact"  # Adjust scopes as needed
}

token_response = requests.post(token_url, headers=headers, data=data)
access_token = token_response.json().get("access_token")

if not access_token:
    raise Exception("Failed to obtain access token.")

print("Access token:", access_token)
