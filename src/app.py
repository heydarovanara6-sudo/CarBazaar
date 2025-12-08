from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, template_folder='../templates', static_folder='../static')

with open('data.json', 'r', encoding='utf-8') as f:
    CARS = json.load(f)

@app.route("/")
def index():
    return render_template('index.html', cars=CARS)

@app.route("/details/<id>")
def details(id):
    car = next((c for c in CARS if c["id"] == id), None)
    return render_template('details.html', car=car) if car else ("Not Found", 404)

@app.route("/api/cars")
def api_cars():
    cars = CARS.copy()
    if brand := request.args.get('brand'): cars = [c for c in cars if c['brand'] == brand]
    if model := request.args.get('model'): cars = [c for c in cars if c['model'] == model]
    if min_p := request.args.get('min_price'): cars = [c for c in cars if c['price'] >= int(min_p)]
    if max_p := request.args.get('max_price'): cars = [c for c in cars if c['price'] <= int(max_p)]
    return jsonify(cars)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
