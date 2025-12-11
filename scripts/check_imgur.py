import os
import requests
import base64
from dotenv import load_dotenv

# Load env vars
load_dotenv()

IMGUR_CLIENT_ID = os.environ.get('IMGUR_CLIENT_ID')
print("--- IMGUR UPLOAD TEST ---")

if not IMGUR_CLIENT_ID:
    print("[ERROR] IMGUR_CLIENT_ID is not set in .env")
    print("Please add: IMGUR_CLIENT_ID=your_id_here")
    print("Get it from: https://api.imgur.com/oauth2/addclient")
else:
    print(f"[OK] Client ID found: {IMGUR_CLIENT_ID[:4]}...{IMGUR_CLIENT_ID[-4:]}")
    
    # Tiny 1x1 pixel red dot
    tiny_img = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
    
    url = "https://api.imgur.com/3/image"
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    
    print("Attempting upload...")
    try:
        response = requests.post(
            url, 
            headers=headers, 
            files={"image": tiny_img},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"[SUCCESS] Image uploaded! URL: {data['data']['link']}")
            else:
                print(f"[FAILURE] API returned success=False: {data}")
        else:
            print(f"[ERROR] HTTP Status {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

print("---------------------------------")
