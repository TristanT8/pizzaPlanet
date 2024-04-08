from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Comment:
    my_db = "pizza_planet"

    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.pizza_id = data['pizza_id']
        self.created_at = data['created_at']
        self.updated_at = data.get('updated_at')

    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO comments (comment_text, pizza_id) VALUES (%(comment_text)s, %(pizza_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)

    @classmethod
    def get_comments_by_pizza_id(cls, pizza_id):
        query = "SELECT * FROM comments WHERE pizza_id = %(pizza_id)s;"
        data = {"pizza_id": pizza_id}
        result = connectToMySQL(cls.my_db).query_db(query, data)
        return [cls(comment) for comment in result]

