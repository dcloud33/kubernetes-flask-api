from flask import Flask, jsonify
import os



app = Flask(__name__)

environment = os.getenv(
    "APP_ENV",
    "development"
)

@app.route("/")
def hello():
    return jsonify({
        "message": "Welcome to my Kubernetes Flask API",
        "environment": environment
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/users")
def users():
    return jsonify([
        {
            "id": 1,
            "name": "Davey Wheeling"
        },
        {
            "id": 2,
            "name": "Jane Smith"
        }
    ])


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000
    )