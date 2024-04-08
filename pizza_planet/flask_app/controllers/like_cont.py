from flask import request, redirect
from flask_app import app
from flask_app.models.like_model import Like

@app.route('/like_pizza', methods=['POST'])
def like_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if user_id and pizza_id:
        Like.like_pizza(user_id, pizza_id)
        # You can handle success or failure here if needed, without flash messages

    return redirect('/dashboard')  # Redirect without flash messages

@app.route('/unlike_pizza', methods=['POST'])
def unlike_pizza():
    user_id = request.form.get('user_id')
    pizza_id = request.form.get('pizza_id')

    if user_id and pizza_id:
        Like.unlike_pizza(user_id, pizza_id)
        # You can handle success or failure here if needed, without flash messages

    return redirect('/dashboard')  # Redirect without flash messages
