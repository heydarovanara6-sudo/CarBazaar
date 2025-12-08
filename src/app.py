from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

# Load cars
with open('data.json', 'r', encoding='utf-8') as f:
    CARS = json.load(f)

@app.route("/")
def index():
    # Simple filtering
    brand = request.args.get('brand', '')
    model = request.args.get('model', '')
    min_price = request.args.get('min', 0, type=int)
    max_price = request.args.get('max', 999999, type=int)
    
    filtered = [c for c in CARS if 
                (not brand or c['brand'] == brand) and
                (not model or c['model'] == model) and
                c['price'] >= min_price and c['price'] <= max_price]
    
    return render_template('index.html', cars=filtered, favorites=[])

@app.route("/details/<id>")
def details(id):
    car = next((c for c in CARS if c["id"] == id), None)
    return render_template('details.html', car=car) if car else ("Not Found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
