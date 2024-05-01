from flask import render_template, request, redirect, url_for, flash
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


from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    my_db = "pizza_planet"

    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.pizza_id = data['pizza_id']

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO comments (comment_text, pizza_id) VALUES (%(comment_text)s, %(pizza_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def get_comments_by_pizza_id(cls, pizza_id):
        query = "SELECT * FROM comments WHERE pizza_id = %(pizza_id)s;"
        data = {"pizza_id": pizza_id}
        results = connectToMySQL(cls.my_db).query_db(query, data)
        comments = []
        for result in results:
            comments.append(cls(result))
        return comments
