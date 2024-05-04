from flask import render_template, request, redirect, url_for, flash, session
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
            return redirect(url_for('view_pizza', pizza_id=pizza_id))

        data = {
            'comment_text': comment_text,
            'pizza_id': pizza_id
        }
        Comment.create_comment(data)
        flash("Comment added successfully.", "comment_success")
        return redirect(url_for('view_pizza', pizza_id=pizza_id))
    else:
        return redirect(url_for('index'))  # Redirect to home if not a POST request or invalid request

@app.route('/edit_comment/<int:comment_id>', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'POST':
        comment_text = request.form['comment']
        
        if not comment_text:
            flash("Comment text is required.", "comment_error")
            return redirect(url_for('edit_comment', comment_id=comment_id))

        comment = Comment.get_comment_by_id(comment_id)
        
        # Check if the current user is the creator of the comment
        if comment.user_id == session.get('user_id'):
            data = {
                'comment_text': comment_text
            }
            Comment.update_comment(comment_id, data)
            flash("Comment updated successfully.", "comment_success")
        else:
            flash("You are not authorized to edit this comment.", "comment_error")

        return redirect(url_for('view_pizza', pizza_id=comment.pizza_id))
    else:
        comment = Comment.get_comment_by_id(comment_id)
        
        # Check if the current user is the creator of the comment
        if comment.user_id == session.get('user_id'):
            return render_template('edit_comment.html', comment=comment)
        else:
            flash("You are not authorized to edit this comment.", "comment_error")
            return redirect(url_for('view_pizza', pizza_id=comment.pizza_id))

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.get_comment_by_id(comment_id)
    
    # Check if the current user is the creator of the comment
    if comment.user_id == session.get('user_id'):
        Comment.delete_comment(comment_id)
        flash("Comment deleted successfully.", "comment_success")
    else:
        flash("You are not authorized to delete this comment.", "comment_error")

    return redirect(url_for('view_pizza', pizza_id=comment.pizza_id))