from flask import request, redirect, url_for, flash, session, render_template
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


@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("You must be logged in to delete a comment.", "error")
        return redirect(url_for('login_user'))

    # Retrieve the comment from the database
    comment = Comment.get_comment_by_id(comment_id)

    # Check if the comment exists
    if not comment:
        flash("Comment not found.", "error")
        return redirect(url_for('pizza_home'))

    # Check if the logged-in user is the creator of the comment
    if comment.user_id != session['user_id']:
        flash("You are not authorized to delete this comment.", "error")
        return redirect(url_for('view_pizza', pizza_id=comment.pizza_id))

    # Delete the comment
    Comment.delete_comment(comment_id)

    flash("Comment deleted successfully.", "success")
    # Redirect to the pizza view page after deleting the comment
    return redirect(url_for('view_pizza', pizza_id=comment.pizza_id))
