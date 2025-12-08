from flask import Flask, render_template, request
import json

app = Flask(__name__)  # Flask automatically finds templates/ in project root

# Load cars
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        CARS = json.load(f)
except:
    CARS = []

@app.route("/")
def index():
    return render_template('index.html', cars=CARS)

@app.route("/details/<id>")
def details(id):
    car = next((c for c in CARS if c["id"] == id), None)
    return render_template('details.html', car=car) if car else ("Car not found", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
