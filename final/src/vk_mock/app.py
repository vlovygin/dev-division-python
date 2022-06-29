import os

from flask import Flask, request, jsonify

app = Flask(__name__)
users = {}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/vk_id/<username>", methods=["GET"])
def get_username(username):
    if username in users:
        return jsonify({"vk_id": users[username]}), 200
    else:
        return jsonify(), 404


@app.route("/vk_id", methods=["POST"])
def create_username():
    request_data = request.get_json()
    username = request_data.get("username", None)
    vk_id = request_data.get("vk_id", None)

    if username in users:
        return jsonify({"error": f"User {username} already exists"}), 400

    if not username:
        return jsonify({"error": "username is required parameter"}), 400
    if not vk_id:
        return jsonify({"error": "vk_id is required parameter"}), 400

    users.update({username: vk_id})
    return jsonify({username: users[username]}), 201


if __name__ == "__main__":
    host = os.environ.get("APP_HOST", "127.0.0.1")
    port = os.environ.get("APP_PORT", "5000")

    app.run(host, port)
