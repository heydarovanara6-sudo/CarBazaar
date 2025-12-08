from flask import Flask, render_template
import json
import os
import re
import urllib.request


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

@app.route("/")
def index():
    return render_template('index.html', cars=CARS)

@app.route("/details/<id>")
def details(id):
    car = next((c for c in CARS if c["id"] == id), None)
    return render_template('details.html', car=car) if car else ("Not found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)