from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({
        "message": "Welcome to my Kubernetes Flask API"
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