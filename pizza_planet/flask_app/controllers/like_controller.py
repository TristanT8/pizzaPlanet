from flask import request, jsonify, flash, redirect
from flask_app import app
from flask_app.models.like_model import Like

@app.route('/like_pizza', methods=['POST'])
def like_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        flash("User ID and Pizza ID are required")
    else:
        success = Like.like_pizza(user_id, pizza_id)
        if success:
            flash("Pizza liked successfully")
        else:
            flash("You already liked this pizza")

    return redirect('/dashboard')  # Redirect after setting the flash message

@app.route('/unlike_pizza', methods=['POST'])
def unlike_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if not user_id or not pizza_id:
        flash("User ID and Pizza ID are required")
    else:
        Like.unlike_pizza(user_id, pizza_id)
        flash("Pizza unliked successfully")

    return redirect('/dashboard')  # Redirect after setting the flash message

