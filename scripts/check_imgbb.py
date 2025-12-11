
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

IMGBB_API_KEY = os.environ.get('IMGBB_API_KEY')
print(f"API Key present: {bool(IMGBB_API_KEY)}")

def upload_test(image_path):
    if not IMGBB_API_KEY:
        print("Error: No API Key")
        return

    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
    }
    
    try:
        with open(image_path, "rb") as file:
            files = {"image": file}
            print(f"Uploading {image_path}...")
            response = requests.post(url, data=payload, files=files, timeout=30)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print(f"SUCCESS! URL: {data['data']['url']}")
                else:
                    print("Upload failed according to API response.")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # Use the image found in artifacts
    img_path = "/home/nargiz/.gemini/antigravity/brain/25671e12-5eb9-45b9-9680-46f5b9964541/uploaded_image_1765477368854.png"
    if os.path.exists(img_path):
        upload_test(img_path)
    else:
        print(f"Test image not found at {img_path}")
