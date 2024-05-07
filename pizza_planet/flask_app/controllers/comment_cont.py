from flask import render_template, request, redirect, flash
from flask_app import app
from flask_app.models.pizza_model import Pizza
from flask_app.models.comment_model import Comment

@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        comment_text = request.form['comment']
        pizza_id = request.form['pizza_id']
        
        if not comment_text:
            flash("Comment text is required.", "comment_error")
            return render_template('view_pizza.html', pizza_id=pizza_id)

        data = {
            'comment_text': comment_text,
            'pizza_id': pizza_id
        }
        Comment.create_comment(data)
        flash("Comment added successfully.", "comment_success")
        return render_template('view_pizza.html', pizza_id=pizza_id)
    else:
        return render_template('home_page.html')  # Redirect to home if not a POST request or invalid request


