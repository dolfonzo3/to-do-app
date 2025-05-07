from flask import Flask, request, jsonify

  app = Flask(__name__)
  todos = []

  @app.route('/set_todos', methods=['POST'])
  def set_todos():
      global todos
      data = request.get_json()
      todos = data.get('items', [])[:10]  # Limit to 10 items
      return jsonify({'status': 'success', 'message': 'To-dos updated.'})

  @app.route('/get_todos', methods=['GET'])
  def get_todos():
      return jsonify({'items': todos})
