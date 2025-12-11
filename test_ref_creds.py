
import cloudinary
import cloudinary.uploader
from io import BytesIO
import base64

# Credentials extracted from debug_prod.py
CLOUD_NAME = "dub9zr9km"
API_KEY = "737748343796794" 
API_SECRET = "LjxRdMF5OdWfH7LV0QM20jX5Org"

print(f"Testing Credentials: Cloud={CLOUD_NAME}, Key={API_KEY}")

try:
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    
    # Tiny 1x1 base64 png
    tiny_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
    
    print("Attempting upload...")
    result = cloudinary.uploader.upload(BytesIO(tiny_png), resource_type="image", folder="verification_test")
    print(f"SUCCESS: Uploaded image. URL: {result.get('secure_url')}")
    
except Exception as e:
    print(f"FAILURE: Error: {e}")
