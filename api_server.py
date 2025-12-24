from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/events", methods=["POST"])
def receive_event():
    data = request.json
    print("Received Event:", data)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000)
