from flask import Flask, request, jsonify, abort
import json
import os

app = Flask(__name__)
TODO_FILE = "todos.json"
API_KEY = os.environ.get("TRMNL_API_KEY")

def load_todos():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)

def is_authorized(req):
    return req.headers.get("x-api-key") == API_KEY

@app.route('/set_todos', methods=['POST'])
def set_todos():
    print("📥 /set_todos called")
    print("🌍 IP address:", request.remote_addr)
    print("🔐 Header received:", request.headers.get("x-api-key"))

    if not is_authorized(request):
        print("⛔ Unauthorized request!")
        abort(403)

    data = request.json
    todos = data.get("items", [])
    save_todos(todos[:10])
    print("💾 Saved todos:", todos[:10])
    return jsonify({"status": "ok", "count": len(todos)})

@app.route('/open_get/<token>', methods=['GET'])
def open_get(token):
    print("📥 /open_get called")
    print("🌍 IP address:", request.remote_addr)

    expected_token = os.getenv("TRMNL_TOKEN")
    print("🔐 Incoming token:", token)
    print("✅ Expected token:", expected_token)

    if token != expected_token:
        print("⛔ Token mismatch!")
        abort(403)

    todos = load_todos()
    print("📦 Sending todos:", todos)
    return jsonify({"items": todos})

@app.route('/get_todos', methods=['GET'])
def get_todos():
    print("📥 /get_todos called")
    print("🌍 IP address:", request.remote_addr)
    print("🔐 Header received:", request.headers.get("x-api-key"))

    if not is_authorized(request):
        print("⛔ Unauthorized request!")
        abort(403)

    todos = load_todos()
    print("📦 Sending todos:", todos)
    return jsonify({"items": todos})
