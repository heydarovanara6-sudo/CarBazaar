from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    """Returns a simple Hello, World! string."""
    return "Welcome to CarBazaar – Buy & Sell Cars in Azerbaijan!"

@app.route("/greet/<name>")
def greet(name):
    """Returns a personalized greeting."""
    return f"Hello, {name}! Looking for a car on CarBazaar?"

@app.route("/car/<int:car_id>")
def car_detail(car_id):
    """Returns a car detail (demo)."""
    return f"Car #{car_id}: Toyota Camry 2023 – $25,000 (Demo)"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
