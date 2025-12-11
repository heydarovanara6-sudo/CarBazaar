
import os
import sys
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import base64

print("--- DIAGNOSTIC V2 START ---")

# 1. Environment Variables
load_dotenv()

# Mirroring app.py sanitization
c_cloud = os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip().replace('"', '').replace("'", "")
c_key = os.environ.get('CLOUDINARY_API_KEY', '').strip().replace('"', '').replace("'", "")
c_secret = os.environ.get('CLOUDINARY_API_SECRET', '').strip().replace('"', '').replace("'", "")

if not c_key.isdigit():
    print(f"[WARNING] API Key contains non-digits: '{c_key}'. Attempting to extract digits.")
    c_key = "".join(filter(str.isdigit, c_key))

print(f"Cloud: {c_cloud}")
print(f"Key: {c_key}")
print(f"Secret: {c_secret[:4]}...{c_secret[-4:]}")

# 2. Cloudinary Upload Test
try:
    cloudinary.config(
        cloud_name=c_cloud,
        api_key=c_key,
        api_secret=c_secret
    )
    # Create a tiny 1x1 base64 png
    tiny_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
    # Upload
    from io import BytesIO
    result = cloudinary.uploader.upload(BytesIO(tiny_png), resource_type="image", folder="carbazaar")
    print(f"SUCCESS: Uploaded test image. URL: {result.get('secure_url')}")
except Exception as e:
    print(f"FAILURE: Cloudinary upload failed. Error: {e}")

print("--- DIAGNOSTIC V2 END ---")
