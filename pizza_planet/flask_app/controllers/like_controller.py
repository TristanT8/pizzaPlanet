from flask import request, jsonify, flash
from flask_app import app
from flask_app.models.like_model import Like

@app.route('/like_pizza', methods=['POST'])
def like_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        return jsonify(message="User ID and Pizza ID are required"), 400

    success = Like.like_pizza(user_id, pizza_id)
    if success:
        return jsonify(message="Pizza liked successfully"), 200
    else:
        flash("You already liked this pizza.")
        return jsonify(message="You already liked this pizza"), 200

@app.route('/unlike_pizza', methods=['POST'])
def unlike_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        return jsonify(message="User ID and Pizza ID are required"), 400

    Like.unlike_pizza(user_id, pizza_id)
    return jsonify(message="Pizza unliked successfully"), 200
