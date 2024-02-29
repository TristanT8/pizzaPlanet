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
        self.meat = pizza_data['meat']
        self.toppings = pizza_data['toppings']
        self.created_at = pizza_data['created_at']
        self.updated_at = pizza_data['updated_at']
        self.user_id = pizza_data['user_id']
        self.creator = None


    @classmethod
    def create_pizza(cls, data):
        query = "INSERT INTO pizza (baker, dough, sauce_base, meat, toppings, user_id) VALUES (%(baker)s, %(dough)s, %(sauce_base)s, %(meat)s, %(toppings)s, %(user_id)s);"
        return connectToMySQL(cls.my_db).query_db(query, data)


    # @classmethod
    