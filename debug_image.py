
import os
import sys
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import base64

# Add src to path if needed (though we imports roughly)
sys.path.append(os.path.join(os.getcwd(), 'src'))

from app import app, db, Car

print("--- DIAGNOSTIC START ---")

# 1. Environment Variables
print("1. Checking Environment Variables...")
load_dotenv()
cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME')
api_key = os.environ.get('CLOUDINARY_API_KEY')
api_secret = os.environ.get('CLOUDINARY_API_SECRET')
db_uri = os.environ.get('SQLALCHEMY_DATABASE_URI')

print(f"CLOUDINARY_CLOUD_NAME: {'SET' if cloud_name else 'MISSING'} ({cloud_name})")
print(f"CLOUDINARY_API_KEY: {'SET' if api_key else 'MISSING'}")
print(f"CLOUDINARY_API_SECRET: {'SET' if api_secret else 'MISSING'}")
print(f"SQLALCHEMY_DATABASE_URI: {'SET' if db_uri else 'MISSING'}")

# 2. Cloudinary Upload Test
print("\n2. Testing Cloudinary Upload...")
if all([cloud_name, api_key, api_secret]):
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        # Create a tiny 1x1 base64 png
        tiny_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
        # Upload
        from io import BytesIO
        result = cloudinary.uploader.upload(BytesIO(tiny_png), resource_type="image", folder="test_debug")
        print(f"SUCCESS: Uploaded test image. URL: {result.get('secure_url')}")
    except Exception as e:
        print(f"FAILURE: Cloudinary upload failed. Error: {e}")
else:
    print("SKIPPING: Cloudinary credentials missing.")

# 3. Database Schema Check
print("\n3. Checking Database Schema...")
with app.app_context():
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        if inspector.has_table('car'):
            columns = [col['name'] for col in inspector.get_columns('car')]
            print(f"Table 'car' columns: {columns}")
            if 'image_url' in columns:
                print("SUCCESS: 'image_url' column exists.")
            else:
                print("FAILURE: 'image_url' column MISSING.")
        else:
            print("FAILURE: Table 'car' does not exist.")
            
        # Check actual rows
        print("Checking recent cars in DB:")
        cars = Car.query.order_by(Car.id.desc()).limit(3).all()
        for car in cars:
            print(f"ID: {car.id}, Brand: {car.brand}, Image URL: {car.image_url}")
            
    except Exception as e:
        print(f"FAILURE: Database check failed. Error: {e}")

print("--- DIAGNOSTIC END ---")
