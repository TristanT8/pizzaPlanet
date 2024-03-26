from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Like:
    my_db = "pizza_planet"


    @classmethod
    def like_pizza(cls, user_id, pizza_id):
        # Check if the user already liked the pizza
        query_check = "SELECT * FROM likes WHERE user_id = %(user_id)s AND pizza_id = %(pizza_id)s"
        result = connectToMySQL(cls.my_db).query_db(query_check, {'user_id': user_id, 'pizza_id': pizza_id})
        if result:
            flash("You already liked this pizza.")
            return False

        # Add like
        query_like = "INSERT INTO likes (user_id, pizza_id) VALUES (%(user_id)s, %(pizza_id)s)"
        connectToMySQL(cls.my_db).query_db(query_like, {'user_id': user_id, 'pizza_id': pizza_id})

        # Update likes_count in pizza table
        query_update_likes = "UPDATE pizza SET likes_count = likes_count + 1 WHERE id = %(pizza_id)s"
        connectToMySQL(cls.my_db).query_db(query_update_likes, {'pizza_id': pizza_id})
        return True


    @classmethod
    def unlike_pizza(cls, user_id, pizza_id):
        # Remove like
        query_unlike = "DELETE FROM likes WHERE user_id = %(user_id)s AND pizza_id = %(pizza_id)s"
        connectToMySQL(cls.my_db).query_db(query_unlike, {'user_id': user_id, 'pizza_id': pizza_id})

        # Update likes_count in pizza table
        query_update_likes = "UPDATE pizza SET likes_count = likes_count - 1 WHERE id = %(pizza_id)s"
        connectToMySQL(cls.my_db).query_db(query_update_likes, {'pizza_id': pizza_id})

