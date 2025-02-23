import streamlit as st
import requests
import os
import base64
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
BASE_API_URL = "https://api.langflow.astra.datastax.com"
FLOW_ID = "4576938a-3247-4c2e-b8aa-f57b07ddf280"
APPLICATION_TOKEN = os.environ.get("APP_TOKEN")

# Function to upload image to API
def upload_image(image_file):
    upload_url = f"{BASE_API_URL}/api/v1/files/upload/{FLOW_ID}"
    
    if not APPLICATION_TOKEN:
        st.error("Missing API token. Please set APP_TOKEN in your environment.")
        return None

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}"}
    files = {"file": (image_file.name, image_file, image_file.type)}

    try:
        response = requests.post(upload_url, files=files, headers=headers)
        if response.status_code == 200:
            return response.json().get("file_path")
        else:
            st.error(f"Error uploading image: {response.text}")
            return None
    except Exception as e:
        st.error(f"Request failed: {str(e)}")
        return None

# Function to send user input and image to API
def run_flow(message: str, file_path: str = None) -> dict:
    api_url = f"{BASE_API_URL}/api/v1/run/{FLOW_ID}?stream=false"
    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}

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

# Convert image to Base64 for inline display
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
#runs search when text is entered:
def run_search(message, uploaded_file):
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
        response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response received.")
        st.success("Search Complete!")
        st.markdown(response_text)
    except Exception as e:
        st.error(str(e))

# Streamlit UI
def main():
    st.set_page_config(page_title="Banana Search", layout="wide")

    # Load Logo
    logo_path = "assets/banana.png"
    img_base64 = get_base64_image(logo_path)

    # Banana Search Layout
    st.markdown(f"""
    <div class="banana-container">
        <div class="banana-header">
            <img src="data:image/png;base64,{img_base64}" alt="Banana Logo" />
            <h1 class="banana-title">Banana Search</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <style>
            /* Button Customization */
            div[data-testid="stButton"] button {
                background-color: #FF5733 !important;  /* Change background color */
                color: white !important;  /* Change text color */
                border-radius: 10px !important;  /* Rounder corners */
                padding: 58px 24px !important;  /* Adjust button size */
                font-size: 36px !important;  /* Increase font size */
                font-weight: bold !important;  /* Make text bold */
                border: none !important;  /* Remove default border */
                transition: 0.3s ease-in-out;  /* Smooth hover effect */
            }
            div[data-testid="stButton"] button:hover {
                background-color: #E64A19 !important;  /* Darker shade on hover */
            }
        </style>
                """, unsafe_allow_html=True)


    
    col1, col2, col3= st.columns([3, 1, 1])


    with col1:
    #    Search bar & Image Upload
        message = st.text_area(label="hi", placeholder="Search Food or Lookup Recipes...", height=135, label_visibility="hidden")
    
    with col2:
        uploaded_file = st.file_uploader(label="hi", type=["png", "jpg", "jpeg"], label_visibility="hidden")
    
    with col3:
        st.markdown(
            """<style> 
                div[data-testid="stButton"] {
                    padding-top: 10px;
                } 
            </style>""", 
            unsafe_allow_html=True
        )
        # Button to process request
        if st.button("Search Foods"):
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
                response_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "No response received.")
                st.success("Search Complete!")
                st.markdown(response_text)
            except Exception as e:
                st.error(str(e))
    
    # UI Styling Overrides
    st.markdown("""
        <style>
            .css-9ycgxx {
                display: none;
            }
            .main .block-container {
                padding: 0;
                max-width: 100% !important;
            }
            body {
                background-color: #ffffff !important;
                color: #000000;
            }
            .banana-container {
                max-width: 1620px;
                margin: 2rem auto;
                background: #ffffff;
                border-radius: 8px;
                padding: 0rem;
            }
            .banana-header {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 1rem;
            }
            .banana-header img {
                height: 150px;
                margin-right: 0.5rem;
            }
            .banana-title {
                font-size: 6rem !important;
                font-weight: 600;
                color: #000;
            }
        </style>
    """,unsafe_allow_html=True)

if __name__ == "__main__":
    main()
