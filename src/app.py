from flask import Flask, render_template
import json
import os
import re
import urllib.parse

try:
    from datasets import load_dataset
except Exception:
    load_dataset = None

try:
    import cloudinary
    from cloudinary import utils as cl_utils
    CLOUDINARY_AVAILABLE = True
except Exception:
    CLOUDINARY_AVAILABLE = False

def cloudinary_fetch_url(raw_url: str):
    """
    Return a Cloudinary fetch URL with f_auto,q_auto if CLOUDINARY env is set.
    Prefers the cloudinary package; falls back to manual URL construction.
    """
    if not raw_url:
        return raw_url

    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME")
    api_key = os.getenv("CLOUDINARY_API_KEY")
    api_secret = os.getenv("CLOUDINARY_API_SECRET")

    if CLOUDINARY_AVAILABLE and cloud_name and api_key and api_secret:
        # Configure once; cloudinary.config is idempotent
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret,
            secure=True,
        )
        try:
            fetch_url, _ = cl_utils.cloudinary_url(
                raw_url,
                type="fetch",
                fetch_format="auto",
                quality="auto",
                secure=True,
            )
            return fetch_url
        except Exception:
            pass

    if cloud_name:
        quoted = urllib.parse.quote(raw_url, safe="")
        return f"https://res.cloudinary.com/{cloud_name}/image/fetch/f_auto,q_auto/{quoted}"

    return raw_url


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

# Flask looks for static/ and templates/ in project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, static_folder='../static', template_folder='../templates')


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


def load_cars_from_hf(dataset_name=None, split=None):
    """Fetch turbo.az dataset from HuggingFace and adapt to our schema."""
    if not load_dataset:
        return None
    dataset_name = dataset_name or os.getenv("HF_DATASET", "vrashad/turbo_az")
    split = split or os.getenv("HF_SPLIT", "train")
    try:
        ds = load_dataset(dataset_name, split=split)

        def first_image(row: dict):
            # Try common keys for image URLs
            for key in ["images", "image", "Image", "Image link", "image_link", "image_url", "Image URL", "photo", "Photo"]:
                if key in row and row.get(key):
                    val = row.get(key)
                    if isinstance(val, list) and val:
                        return str(val[0])
                    if isinstance(val, str):
                        return val
            # Some datasets might store a single image URL under 'Link' (if it's direct)
            if "Link" in row and isinstance(row.get("Link"), str) and row.get("Link").startswith("http"):
                return row.get("Link")
            return None

        cars = []
        for idx, row in enumerate(ds):
            price, currency = parse_price(row.get("Price"))
            engine = parse_engine(row.get("Engine"))
            odometer = parse_odometer(row.get("Distance"))
            name = row.get("Name", "")
            parts = name.split(" ", 1)
            brand = parts[0] if parts else "Unknown"
            model = parts[1] if len(parts) > 1 else parts[0] if parts else "Unknown"
            image = first_image(row) or BRAND_IMAGE_MAP.get(brand, "https://via.placeholder.com/400x300?text=Car")
            image = cloudinary_fetch_url(image) or image
            cars.append(
                {
                    "id": str(idx + 1000),
                    "brand": brand,
                    "model": model,
                    "year": str(row.get("Year", "")),
                    "price": price,
                    "currency": currency,
                    "engine": engine,
                    "odometer": odometer,
                    "city": row.get("City", "Baku"),
                    "dates": row.get("Classified Date", "Today") or row.get("dates", "Today"),
                    "images": [image],
                }
            )
        return cars
    except Exception:
        return None


# Load cars: try configured HF dataset, fall back to the original zmmmdf/turbo.az, then empty
CARS = load_cars_from_hf() or load_cars_from_hf("zmmmdf/turbo.az") or []

@app.route("/")
def index():
    return render_template('index.html', cars=CARS)

@app.route("/details/<id>")
def details(id):
    car = next((c for c in CARS if c["id"] == id), None)
    return render_template('details.html', car=car) if car else ("Not found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)