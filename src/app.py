from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "CarBazaar is LIVE on Render! Auto-deploy WORKS!"

@app.route("/greet/<name>")
def greet(name):
    return f"Salam, {name}! Welcome to CarBazaar — Turbo.az clone coming soon!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
