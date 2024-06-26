from flask_app.config.mysqlconnection import connectToMySQL

class Comment:
    my_db = "pizza_planet"

    def __init__(self, data):
        self.id = data['id']
        self.comment_text = data['comment_text']
        self.pizza_id = data['pizza_id']
        self.user_id = data['user_id']


    @classmethod
    def create_comment(cls, data):
        query = "INSERT INTO comments (comment_text, pizza_id, user_id) VALUES (%(comment_text)s, %(pizza_id)s, %(user_id)s);"
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


    @classmethod
    def get_comment_by_id(cls, comment_id):
        query = "SELECT * FROM comments WHERE id = %(comment_id)s;"
        data = {"comment_id": comment_id}
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if result:
            return cls(result[0])  # Return the first comment object if found
        else:
            return None


    @classmethod
    def delete_comment(cls, comment_id):
        query = "DELETE FROM comments WHERE id = %(comment_id)s;"
        data = {'comment_id': comment_id}
        return connectToMySQL(cls.my_db).query_db(query, data)
