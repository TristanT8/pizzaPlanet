from flask import request, jsonify, flash, redirect
from flask_app import app
from flask_app.models.like_model import Like

@app.route('/like_pizza', methods=['POST'])
def like_pizza():
    # Your existing code for liking a pizza post
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        flash("User ID and Pizza ID are required")
        return redirect('/dashboard')  # Redirect to home screen

    success = Like.like_pizza(user_id, pizza_id)
    if success:
        flash("Pizza liked successfully")
    else:
        flash("You already liked this pizza")

    return redirect('/dashboard')  # Redirect to home screen

@app.route('/unlike_pizza', methods=['POST'])
def unlike_pizza():
    # Your existing code for unliking a pizza post
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        flash("User ID and Pizza ID are required")
        return redirect('/dashboard')  # Redirect to home screen

    Like.unlike_pizza(user_id, pizza_id)
    flash("Pizza unliked successfully")

    return redirect('/dashboard')  # Redirect to home screen
