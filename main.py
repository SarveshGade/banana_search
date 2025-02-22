import requests
import json

# Replace with your Langflow base URL and flow ID
LANGFLOW_URL = "https://api.langflow.astra.datastax.com"
FLOW_ID = "a430cc57-06bb-4c11-be39-d3d4de68d2c4"  # Use your actual flow ID

# -----------------------------
# Step 1: Upload the image file
# -----------------------------
upload_url = f"{LANGFLOW_URL}/api/v1/files/upload/{FLOW_ID}"

# Make sure the file exists and the path is correct
image_file_path = "cv/frij.jpg"  # Replace with your file path

with open(image_file_path, "rb") as file_obj:
    # requests will set the correct multipart/form-data header automatically
    response = requests.post(upload_url, files={"file": file_obj})

# Check the upload response
upload_response = response.json()
print("Upload response:", json.dumps(upload_response, indent=2))

# The response should include a file_path like:
# "file_path": "a430cc57-06bb-4c11-be39-d3d4de68d2c4/2024-11-27_14-47-50_image-file.png"
file_path_value = upload_response.get("file_path")
if not file_path_value:
    raise ValueError("File upload did not return a valid file_path.")

# ------------------------------------------------
# Step 2: Run the flow, passing the file reference
# ------------------------------------------------
run_url = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false"

# Create the payload with tweaks; update the component name if needed.
payload = {
    "output_type": "chat",
    "input_type": "chat",
    "tweaks": {
        "ChatInput-b67sL": {
            "files": file_path_value,
            "input_value": "what do you see?"
        }
    }
}

headers = {"Content-Type": "application/json"}

# Send the POST request to run the flow
response_run = requests.post(run_url, headers=headers, json=payload)
print("Run response:", json.dumps(response_run.json(), indent=2))