import os
import requests
from dotenv import load_dotenv

# Load env vars
load_dotenv()

UNSPLASH_ACCESS_KEY = os.environ.get('UNSPLASH_ACCESS_KEY')
print("--- UNSPLASH INTEGRATION TEST ---")

if not UNSPLASH_ACCESS_KEY:
    print("[ERROR] UNSPLASH_ACCESS_KEY is not set in .env")
    print("Please add: UNSPLASH_ACCESS_KEY=your_key_here")
    print("(Waiting for your email confirmation...)")
else:
    print(f"[OK] Key found: {UNSPLASH_ACCESS_KEY[:4]}...{UNSPLASH_ACCESS_KEY[-4:]}")
    
    query = "BMW X5 car"
    print(f"Testing Unsplash Search for: '{query}'...")
    
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": 1,
        "per_page": 1,
        "orientation": "landscape",
        "client_id": UNSPLASH_ACCESS_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                img_url = data['results'][0]['urls']['regular']
                print(f"[SUCCESS] Unsplash Image found: {img_url}")
            else:
                print("[WARNING] No results found for query.")
        elif response.status_code == 401:
            print("[ERROR] Unauthorized. Check your Access Key.")
        else:
            print(f"[ERROR] API returned status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"[ERROR] Exception occurred: {e}")

print("---------------------------------")
