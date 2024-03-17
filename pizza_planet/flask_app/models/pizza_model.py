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
        self.updated_at = pizza_data['updated_at']
        self.user_id = pizza_data['user_id']
        self.creator = None


    @classmethod
    def create_pizza(cls, data):
        data['sauce_base'] = ', '.join(data.getlist('sauce_base'))
        data['cheese'] = ', '.join(data.getlist('cheese'))
        data['meat'] = ', '.join(data.getlist('meat'))
        data['vegetables'] = ', '.join(data.getlist('vegetables'))
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
    def get_all_pizzas(cls):
        query = "SELECT * FROM pizza JOIN users ON pizza.user_id = users.id"
        result = connectToMySQL(cls.my_db).query_db(query)
        if not result:
            return []
        all_pizzas = []
        for row in result:
            single_pizza = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
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