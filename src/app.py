from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import re
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Flask looks for static/ and templates/ in project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# PROJECT_ROOT is the parent of src/ (i.e., /home/nargiz/CarBazaar)
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))

app = Flask(__name__, 
            static_folder=os.path.join(PROJECT_ROOT, 'static'), 
            template_folder=os.path.join(PROJECT_ROOT, 'templates'))
app.secret_key = 'some_secret_key_for_session_management' # Change this in production!

# Database Configuration
# Use environment variable for DB URI (production), fallback to SQLite (dev)
default_db = f'sqlite:///{os.path.join(PROJECT_ROOT, "users.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', default_db)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 280,
    "pool_timeout": 20,
}

# Imgur Configuration
# ImgBB Configuration
def upload_to_imgbb(file_storage):
    """
    Upload a file to ImgBB.
    Returns (url, error_message).
    """
    # Fetch at runtime to ensure we get the latest env var
    api_key = os.environ.get('IMGBB_API_KEY')
    
    if not api_key:
        # Debugging: Print keys to see if we have a typo (safe, prompt only shows keys)
        print(f"[DEBUG] API Key missing. Env keys: {list(os.environ.keys())}") 
        return None, "ImgBB API Key missing from configuration"
        
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": api_key,
    }
    
    try:
        # Read file content
        file_storage.seek(0)
        file_content = file_storage.read()
        
        # ImgBB expects 'image' form field
        files = {
            "image": file_content
        }
        
        response = requests.post(
            url, 
            data=payload, 
            files=files,
            timeout=30
        )
        
        try:
            data = response.json()
        except:
             return None, f"Invalid JSON response: {response.text[:100]}"

        if response.status_code == 200 and data.get('success'):
            return data['data']['url'], None
        else:
            error_msg = data.get('error', {}).get('message', 'Unknown ImgBB error')
            return None, f"ImgBB Error: {error_msg}"
            
    except Exception as e:
        return None, f"Upload Exception: {str(e)}"



db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Usage: Association Table for User-Car Favorites
favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('car_id', db.Integer, db.ForeignKey('car.id'), primary_key=True)
)


# User Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)
    favorited_cars = db.relationship('Car', secondary=favorites, backref=db.backref('favorited_by', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Car Model
from datetime import datetime
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(3), default='AZN')
    engine = db.Column(db.Float, default=0.0)
    odometer = db.Column(db.Integer, default=0)
    city = db.Column(db.String(50), default='Baku')
    image_url = db.Column(db.String(500)) # Store Image URL (External)
    contact_number = db.Column(db.String(50)) # Increased to 50 chars
    views = db.Column(db.Integer, default=0)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def images(self):
        # Helper to return list of images (compatible with existing template logic)
        if self.image_url:
            return [self.image_url]
        return ["https://via.placeholder.com/400x300?text=No+Image"]
    
    @property
    def dates(self):
        # Format date for display
        return self.date_posted.strftime("%Y-%m-%d")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def safe_image(url: str, brand: str = "Unknown"):
    """
    Ensure we return a usable image URL:
    - Use provided URL if it's an http/https link.
    - Otherwise, fall back to brand image, then placeholder.
    """
    candidate = url if (isinstance(url, str) and url.startswith("http")) else None
    if not candidate:
        candidate = BRAND_IMAGE_MAP.get(brand, PLACEHOLDER_IMG)
    return candidate or PLACEHOLDER_IMG


PLACEHOLDER_IMG = "https://via.placeholder.com/400x300?text=No+Image"

# Brand-level image fallbacks (one representative image per brand)
BRAND_IMAGE_MAP = {
    "Abarth": "https://turbo.azstatic.com/uploads/f710x568/2023%2F01%2F11%2F11%2F19%2F41%2F5f34c8eb-5138-4d0c-b78e-8c817d98aa5f%2F52522_Mu2ZZs1LqQkRDJpgK-R_xw.jpg",
    "Audi": "https://turbo.azstatic.com/uploads/f710x568/2022%2F08%2F31%2F23%2F10%2F15%2F729c8b30-ea56-45d3-bdf7-f8a7b0e9e950%2F3015_eyJujDX3UzCcNboINLPl_g.jpg",
    "Toyota": "https://turbo.azstatic.com/uploads/full/2022%2F12%2F22%2F10%2F26%2F59%2F9f754715-d306-49f2-b2e2-60ab36f771e6%2F80870_wrsWRRQ-A4ySXmcF4jOpXg.jpg",
    "Ford": "https://turbo.azstatic.com/uploads/full/2023%2F01%2F29%2F15%2F18%2F37%2F46fbb03a-0cd9-4409-bbc6-03023e588329%2F67200_jmTFoB8S36kCqexBERvuhA.jpg",
    "Bestune": "https://turbo.azstatic.com/uploads/full/2022%2F09%2F19%2F17%2F33%2F45%2F027df0e9-c5df-46a1-8428-2a356ee17d45%2F44832_yspkMx-Q-VQPULaAOI_MSw.jpg",
    "Honggi": "https://turbo.azstatic.com/uploads/full/2022%2F04%2F19%2F15%2F59%2F38%2F716b705f-e564-4d55-995a-7762e6881f4c%2F5883_vLXDlraa-zAkIkuXUdl05w.jpg",
    "Kia": "https://turbo.azstatic.com/uploads/full/2022%2F10%2F20%2F20%2F19%2F37%2Ff0d40936-67d4-47b2-8f88-39e95c546ae3%2F57379_yzPNLn7TAwj6RDByWKgvOA.jpg",
    "Mercedes": "https://turbo.azstatic.com/uploads/f710x568/2023%2F01%2F31%2F21%2F26%2F41%2Fa8168d7c-d02e-495f-8f01-69fcdc5e3e03%2F11997_tG1Qr36Aqkf171mt0oZG7Q.jpg",
    "Chevrolet": "https://turbo.azstatic.com/uploads/full/2022%2F09%2F16%2F12%2F50%2F42%2Febf8e8a9-4b9e-42d1-bb0c-725555a056e1%2F54915_qtOrHDVrjjW3-GNgDyN8vg.jpg",
    "Jaguar": "https://turbo.azstatic.com/uploads/f710x568/2023%2F01%2F30%2F20%2F01%2F36%2Fb8325e8f-b0b1-4423-8163-59ab513c0445%2F49759_qjtKYlmSfvuA_6JFNFa8AQ.jpg",
    "C.Moto": "https://turbo.azstatic.com/uploads/full/2023%2F01%2F31%2F16%2F42%2F46%2Fb60abf3c-aff7-450d-b793-bf93ceff3a06%2F15660_QvgVQpBtt9j4-9bpnj5N8Q.jpg",
    "Tayota": "https://turbo.azstatic.com/uploads/full/2023%2F01%2F24%2F14%2F33%2F40%2F0f9b3be6-4ae5-417a-bcf1-db0f39927d4e%2F33485_P0YBt9TmP9pEv29rCuhWLg.jpg",
    "Porsche": "https://turbo.azstatic.com/uploads/full/2023%2F02%2F01%2F01%2F26%2F17%2Ffb77794e-9d37-424e-944d-3b233bc03467%2F12003_RjupQqZAh9kZFu-IaHqJ7g.jpg",
    "Paz": "https://turbo.azstatic.com/uploads/full/2023%2F01%2F23%2F21%2F49%2F47%2F18227380-ca87-4ecc-8497-3c972bce2db1%2F42127_wKRyc3J6-wogJe-WZMY-ug.jpg",
    "Ferrari": "https://turbo.azstatic.com/uploads/f710x568/2022%2F12%2F28%2F15%2F40%2F48%2Fb18d5c9e-58d7-4e2e-9bba-1c29cbce9940%2F61425_r8Og48iy5Jr9GvOTtAnnyQ.jpg",
    "Acura": "https://turbo.azstatic.com/uploads/full/2023%2F01%2F31%2F13%2F41%2F14%2F30be4e7e-c9ac-455d-8616-616f096d6da7%2F71593_f9yNl7lW4FO-spgOift6dw.jpg",
}


def parse_price(raw: str):
    """Return (price, currency) from strings like '63 500 $' or '65 900 AZN'."""
    if not raw:
        return 0, "AZN"
    currency = "AZN"
    if "AZN" in raw.upper():
        currency = "AZN"
    elif "$" in raw:
        currency = "USD"
    elif "€" in raw or "EUR" in raw.upper():
        currency = "EUR"
    digits = re.sub(r"[^\d.]", "", raw)
    try:
        return float(digits), currency
    except ValueError:
        return 0, currency


def parse_engine(raw: str):
    """Extract numeric engine size like '2.0 L' -> 2.0."""
    if not raw:
        return 0.0
    digits = re.match(r"([0-9]+(?:\.[0-9]+)?)", raw.replace(",", "."))
    return float(digits.group(1)) if digits else 0.0


def parse_odometer(raw: str):
    """Extract km value like '130 000 km' -> 130000."""
    if not raw:
        return 0
    digits = re.sub(r"[^\d]", "", raw)
    try:
        return int(digits)
    except ValueError:
        return 0


def load_cars_from_js(js_url=None):
    """
    Fetch cars from a JS file (const data = [...]) and adapt to our schema.
    Default source: GitHub raw data.js with image links.
    """
    src = js_url or os.getenv(
        "JS_DATA_URL",
        "https://raw.githubusercontent.com/aysumaharramovaa/turbo-az/main/data.js",
    )
    try:
        with urllib.request.urlopen(src, timeout=15) as resp:
            text = resp.read().decode("utf-8")
    except Exception:
        return None

    # Extract array contents
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1:
        return None
    body = text[start : end + 1]

    # Remove trailing commas before closing brackets/braces
    body = re.sub(r",\s*]", "]", body)
    body = re.sub(r",\s*}", "}", body)

    # Quote object keys without touching URLs
    body = re.sub(
        r"(?P<prefix>[{,]\s*)(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*:",
        r'\g<prefix>"\g<key>":',
        body,
    )

    try:
        arr = json.loads(body)
    except Exception:
        return None

    cars = []
    for idx, row in enumerate(arr):
        brand = row.get("brand", "Unknown")
        model = row.get("model", brand)
        price = row.get("price", 0)
        currency = row.get("currency", "AZN")
        engine = row.get("engine", 0)
        odometer = row.get("odometer", 0)
        city = row.get("city", "Baku")
        year = row.get("year", "")
        dates = row.get("dates", "Today")
        images = row.get("images") or []
        img = images[0] if images else None
        img = safe_image(img, brand)
        cars.append(
            {
                "id": str(row.get("id", idx + 5000)),
                "brand": brand,
                "model": model,
                "year": str(year),
                "price": price,
                "currency": currency,
                "engine": engine,
                "odometer": odometer,
                "city": city,
                "dates": dates,
                "images": [img],
            }
        )
    return cars


def load_cars_from_hf(*args, **kwargs):
    return None


# Load cars only from JS dataset
CARS = load_cars_from_js() or []

from werkzeug.utils import secure_filename
import uuid

@app.route("/")
def index():
    # Fetch DB cars first
    db_cars = Car.query.order_by(Car.date_posted.desc()).all()
    # Merge with demo cars (demo cars come after? or before? Let's put DB cars first)
    all_cars = list(db_cars) + list(CARS)
    
    # Pre-fetch favorites for efficiency
    fav_ids = []
    if current_user.is_authenticated:
        fav_ids = [c.id for c in current_user.favorited_cars]
        
    return render_template('index.html', cars=all_cars, fav_ids=fav_ids)


@app.route("/details/<id>")
def details(id):
    car = None
    # Try finding in DB if id is numeric (DB uses integer IDs)
    if id.isdigit():
        car = Car.query.filter_by(id=int(id)).first()
    
    if not car:
        # Fallback to demo cars (ids are strings like "5000")
        car = next((c for c in CARS if str(c["id"]) == str(id)), None)
    
    if car and isinstance(car, Car): # Only increment for DB cars
        car.views += 1
        db.session.commit()
        
    return render_template('details.html', car=car) if car else ("Not found", 404)

@app.route("/add_car", methods=["POST"])
@login_required
def add_car():
    brand = request.form.get("brand")
    model = request.form.get("model")
    contact_number = request.form.get("contact_number")
    try:
        year = int(request.form.get("year"))
        price = int(request.form.get("price"))
        engine = float(request.form.get("engine") or 0)
        odometer = int(request.form.get("odometer") or 0)
    except ValueError:
        flash("Invalid numeric data")
        return redirect(url_for('index'))

    city = request.form.get("city")
    currency = request.form.get("currency")
    
    # Handle Image - Upload to ImgBB
    file = request.files.get('images')
    image_url = None
    upload_error = None
    
    if file and file.filename:
        print(f"[DEBUG] Uploading file: {file.filename}")
        image_url, upload_error = upload_to_imgbb(file)
        
        if image_url:
            flash("Image uploaded successfully!", "success")
        else:
            flash(f"Image upload failed: {upload_error}", "error")
    else:
        print("[DEBUG] No image file provided")


    new_car = Car(
        brand=brand,
        model=model,
        year=year,
        price=price,
        currency=currency,
        engine=engine,
        odometer=odometer,
        city=city,
        contact_number=contact_number, # Added contact number
        image_url=image_url,
        owner=current_user
    )
    
    try:
        db.session.add(new_car)
        db.session.commit()
        print(f"[DEBUG] Car saved to DB with ID: {new_car.id}, Image URL: {new_car.image_url}")
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Failed to save car: {e}")
        flash(f"Error saving car: {e}", "error")
        return redirect(url_for('index'))
    
    if image_url:
        flash(f"Car added successfully with image!", "success")
    else:
        flash(f"Car added successfully (no image uploaded)", "info")
    return redirect(url_for('index'))

@app.route("/my_ads")
@login_required
def my_ads():
    # Fetch cars belonging to current user
    user_cars = Car.query.filter_by(user_id=current_user.id).order_by(Car.date_posted.desc()).all()
    return render_template('my_ads.html', cars=user_cars)

@app.route("/delete_car/<int:car_id>", methods=["POST"])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    
    # Verify ownership
    if car.user_id != current_user.id:
        flash("You can only delete your own ads!")
        return redirect(url_for('my_ads'))
    
    # Delete the car
    # First remove from favorites to avoid FK error
    db.session.execute(favorites.delete().where(favorites.c.car_id == car.id))
    db.session.delete(car)
    db.session.commit()
    flash("Ad deleted successfully!")
    return redirect(url_for('my_ads'))

@app.route("/delete_all_ads", methods=["POST"])
@login_required
def delete_all_ads():
    # Delete all cars belonging to current user
    try:
        # 1. Get IDs of cars to be deleted
        cars_to_delete = Car.query.filter_by(user_id=current_user.id).all()
        car_ids = [c.id for c in cars_to_delete]
        
        if car_ids:
            # 2. Delete from favorites
            db.session.execute(favorites.delete().where(favorites.c.car_id.in_(car_ids)))
            
            # 3. Delete cars
            for car in cars_to_delete:
                db.session.delete(car)
                
            db.session.commit()
            flash(f"Deleted all {len(car_ids)} ads successfully!", "success")
        else:
            flash("No ads to delete.", "info")

    except Exception as e:

        db.session.rollback()
        flash(f"Error deleting ads: {str(e)}", "error")
        
    return redirect(url_for('my_ads'))

@app.route("/toggle_favorite/<int:car_id>", methods=["POST"])
@login_required
def toggle_favorite(car_id):
    car = Car.query.get_or_404(car_id)
    if car in current_user.favorited_cars:
        current_user.favorited_cars.remove(car)
        flash("Removed from favorites", "info")
    else:
        current_user.favorited_cars.append(car)
        flash("Added to favorites!", "success")
    db.session.commit()
    # Redirect back to the page the user came from, or index if unknown
    return redirect(request.referrer or url_for('index'))

@app.route("/favorites")
@login_required
def favorites():
    cars = current_user.favorited_cars
    return render_template('favorites.html', cars=cars)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")
    return render_template('login.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if user already exists
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash("User already exists!")
            return redirect(url_for('register'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        return redirect(url_for('index'))
        
    return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


from sqlalchemy import text
from sqlalchemy.exc import OperationalError

def run_migrations():
    """Auto-migrate database schema changes for local dev."""
    with app.app_context():
        try:
            # Add 'views' column if missing
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE car ADD COLUMN views INTEGER DEFAULT 0"))
                conn.commit()
            print("Migrated: Added 'views' column.")
        except OperationalError:
            pass # Column likely exists

        try:
            # Add 'contact_number' column if missing
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE car ADD COLUMN contact_number VARCHAR(50)"))
                conn.commit()
            print("Migrated: Added 'contact_number' column.")
        except OperationalError:
            pass # Column likely exists

# Create tables if they don't exist (for tests and first run)
with app.app_context():
    db.create_all()
    run_migrations() # Run migrations on startup

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)