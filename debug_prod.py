
import os
import sys
import cloudinary
import cloudinary.uploader
import base64
from sqlalchemy import create_engine, text, inspect

# User's Production Credentials (from screenshot)
# NOTE: We use these solely to diagnose the remote system.
DB_URI = "mysql+pymysql://nargiz:azuf58Namny@sql-nargiz.alwaysdata.net/nargiz_carbazaar"
CLOUD_NAME = "dub9zr9km"
API_KEY = "737748343796794"
API_SECRET = "LjxRdMF5OdWfH7LV0QM20jX5Org"

print("--- PRODUCTION DIAGNOSTIC START ---")

# 1. Connection Test & Schema Check
print("\n1. Connecting to Remote Database...")
try:
    engine = create_engine(DB_URI)
    with engine.connect() as conn:
        print("SUCCESS: Connected to database.")
        
        inspector = inspect(engine)
        if inspector.has_table('car'):
            columns = [col['name'] for col in inspector.get_columns('car')]
            print(f"Table 'car' columns: {columns}")
            
            if 'image_url' in columns:
                print("SUCCESS: 'image_url' column exists.")
            else:
                print("FAILURE: 'image_url' column MISSING.")
                
                # ATTEMPT AUTOMATIC FIX
                print(">>> ATTEMPTING TO FIX: Adding 'image_url' column...")
                try:
                    conn.execute(text("ALTER TABLE car ADD COLUMN image_url VARCHAR(500)"))
                    conn.commit() # Important for SQLAlchemy 2.0+ (or 1.4+ with future)
                    print(">>> SUCCESS: Column 'image_url' added!")
                except Exception as e:
                    print(f">>> FAILED to add column: {e}")
        else:
            print("FAILURE: Table 'car' does not exist.")
            
except Exception as e:
    print(f"FAILURE: Database Connection Error: {e}")
    # Note: If pymysql is missing locally, we need to install it.
    print("Hint: If 'No module named pymysql', we need to install it in the environment.")


# 2. Cloudinary Credentials Check
print("\n2. Testing Cloudinary Credentials (Production)...")
try:
    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    # Upload Tiny Image
    tiny_png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
    from io import BytesIO
    result = cloudinary.uploader.upload(BytesIO(tiny_png), resource_type="image", folder="prod_debug")
    print(f"SUCCESS: Uploaded to Production Cloudinary. URL: {result.get('secure_url')}")
except Exception as e:
    print(f"FAILURE: Production Cloudinary credentials failed. Error: {e}")

print("--- PRODUCTION DIAGNOSTIC END ---")
