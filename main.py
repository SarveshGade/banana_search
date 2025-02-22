# Note: Replace **<YOUR_APPLICATION_TOKEN>** with your actual Application token

import requests
from dotenv import load_dotenv
import os
import streamlit as st


load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "dcbab69c-68d2-4b67-9c89-1b5ec6803b26"
FLOW_ID = "4576938a-3247-4c2e-b8aa-f57b07ddf280"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-QMZYv": {},
  "OpenAIModel-HHR0J": {},
  "Prompt-wyeZn": {}
}

def upload_image(image_file):
    """Uploads an image to Langflow and returns the file path."""
    upload_url = f"{BASE_API_URL}/api/v1/files/upload/{FLOW_ID}"
    
    # Ensure token is valid
    if not APPLICATION_TOKEN:
        st.error("Missing API token. Please set APP_TOKEN in your environment.")
        return None

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}"}
    
    files = {"file": (image_file.name, image_file, image_file.type)}
    
    # Debugging print statements
    print(f"Uploading to: {upload_url}")
    print(f"Headers: {headers}")
    print(f"File Name: {image_file.name}, Type: {image_file.type}")

    try:
        response = requests.post(upload_url, files=files, headers=headers)
        print("Response Status:", response.status_code)
        print("Response Text:", response.text)  # See full error message
        
        if response.status_code == 200:
            return response.json().get("file_path")
        else:
            st.error(f"Error uploading image: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None


def run_flow(message: str, file_path: str = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}?stream=false"
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "tweaks": {
            "ChatInput-QMZYv": {
                "input_value": message,
                "files": file_path if file_path else ""
            }
        }
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def main():
    st.title("Chat Interface")
    message = st.text_area("Message", placeholder="Ask something...")
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    
    if st.button("Run Flow"):
        if not message.strip():
            st.error("Please enter a message")
            return

        file_path = None
        if uploaded_file:
            st.info("Uploading image...")
            file_path = upload_image(uploaded_file)
            if not file_path:
                return  # Stop if image upload fails

        try:
            with st.spinner("Running AI analysis..."):
                response = run_flow(message, file_path)
            response_text = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
            st.markdown(response_text)
        except Exception as e:
            st.error(str(e))
            
if __name__ == "__main__":
    main()

