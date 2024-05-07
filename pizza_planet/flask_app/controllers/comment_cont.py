from flask import request, redirect, url_for, flash, session
from flask_app import app
from flask_app.models.pizza_model import Pizza
from flask_app.models.comment_model import Comment

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        comment_text = request.form['comment']
        pizza_id = request.form['pizza_id']
        user_id = session.get('user_id')  # Get user_id from session

        if not comment_text:
            flash("Comment text is required.", "comment_error")
            return redirect(url_for('view_pizza', pizza_id=pizza_id))

        data = {
            'comment_text': comment_text,
            'pizza_id': pizza_id,
            'user_id': user_id  # Include user_id in data
        }
        Comment.create_comment(data)
        flash("Comment added successfully.", "comment_success")
        return redirect(url_for('view_pizza', pizza_id=pizza_id))
    else:
        return redirect(url_for('index'))  # Redirect to home if not a POST request or invalid request


