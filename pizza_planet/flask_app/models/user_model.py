from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    my_db = "Pizza_planet"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_user(cls, form_data):
        hash_password = bcrypt.generate_password_hash(form_data['password'])
        print(hash_password)
        user_data = {
            "first_name" : form_data['first_name'],
            "last_name" : form_data['last_name'],
            "email" : form_data['email'],
            "password" : hash_password
        }

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(cls.my_db).query_db(query, user_data)
        print(form_data)
        print(user_data)
        return result


