from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask import flash


class Pizza:
    my_db = "pizza_planet"
    def __init__(self, pizza_data):
        self.id = pizza_data['id']
        self.baker = pizza_data['baker']
        self.dough = pizza_data['dough']
        self.sauce_base = pizza_data['sauce_base']
        self.cheese = pizza_data['cheese']
        self.meat = pizza_data['meat']
        self.vegetables = pizza_data['vegetables']
        self.created_at = pizza_data['created_at']
        self.updated_at = pizza_data.get('updated_at')  # Handle missing 'updated_at'
        self.user_id = pizza_data['user_id']
        self.likes_count = pizza_data['likes_count']
        self.creator = None


    @classmethod
    def create_pizza(cls, data):
        query = "INSERT INTO pizza (baker, dough, sauce_base, cheese, meat, vegetables, user_id) VALUES (%(baker)s, %(dough)s, %(sauce_base)s, %(cheese)s,  %(meat)s, %(vegetables)s, %(user_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)


    @classmethod
    def get_pizza(cls, data):
        query = "SELECT * FROM pizza WHERE pizza.id = %(id)s"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if not result:
            return None
        pizza_data = result[0]
        pizza_data['sauce_base'] = pizza_data['sauce_base'].split(', ')
        pizza_data['cheese'] = pizza_data['cheese'].split(', ')
        pizza_data['meat'] = pizza_data['meat'].split(', ')
        pizza_data['vegetables'] = pizza_data['vegetables'].split(', ')
        return cls(pizza_data)


    @classmethod
    def get_all_pizzas(cls, user_id):
        query = """
            SELECT pizza.*, users.id AS user_id, users.first_name, users.last_name, users.email, users.password, users.created_at AS user_created_at, users.updated_at AS user_updated_at,
            IFNULL(l.likes_count, 0) AS likes_count,
            CASE WHEN l.user_id IS NOT NULL THEN 1 ELSE 0 END AS liked_by_user
            FROM pizza
            JOIN users ON pizza.user_id = users.id
            LEFT JOIN (
                SELECT pizza_id, COUNT(*) AS likes_count
                FROM likes
                GROUP BY pizza_id
            ) l ON pizza.id = l.pizza_id
            LEFT JOIN likes ON pizza.id = likes.pizza_id AND likes.user_id = %(user_id)s
        """
        data = {'user_id': user_id}
        result = connectToMySQL(cls.my_db).query_db(query, data)
        if not result:
            return []
        all_pizzas = []
        for row in result:
            single_pizza = cls(row)
            user_data = {
                "id": row['user_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['user_created_at'],
                "updated_at": row['user_updated_at']
            }
            single_pizza.creator = User(user_data)
            all_pizzas.append(single_pizza)
        return all_pizzas



    @classmethod
    def update_pizza(cls, data):
        query = "UPDATE pizza SET baker = %(baker)s, dough = %(dough)s, sauce_base = %(sauce_base)s, cheese = %(cheese)s,  meat = %(meat)s, vegetables = %(vegetables)s;"
        result = connectToMySQL(cls.my_db).query_db(query, data)
        return result


    @classmethod
    def delete_pizza(cls, data):
        query = "DELETE FROM pizza WHERE pizza.id = %(id)s;"
        return connectToMySQL(cls.my_db).query_db(query, data)


    @staticmethod
    def validate_pizza(pizza_data):
        is_valid = True
        if len(pizza_data['baker']) < 3:
            flash("Baker name must be at least 3 characters long.")
            is_valid = False
        if not pizza_data.getlist('dough'):
            flash("Please select which dough you'd like.")
            is_valid = False
        if not pizza_data.getlist('sauce_base'):
            flash("Please select which sauce you'd like.")
            is_valid = False
        if not pizza_data.getlist('cheese'):
            flash("Please select which cheese you'd like.")
            is_valid = False
        if not pizza_data.getlist('meat'):
            flash("Please select which protein you'd like.")
            is_valid = False
        if not pizza_data.getlist('vegetables'):
            flash("Please choose your veggies.")
            is_valid = False
        return is_valid