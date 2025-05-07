from flask import Flask, request, jsonify, abort
import json
import os

app = Flask(__name__)
TODO_FILE = "todos.json"
import os
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
    if not is_authorized(request):
        abort(403)
    data = request.json
    todos = data.get("items", [])
    save_todos(todos[:10])
    return jsonify({"status": "ok", "count": len(todos)})

@app.route('/get_todos', methods=['GET'])
def get_todos():
    if not is_authorized(request):
        abort(403)
    return jsonify({"items": load_todos()})
