from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User


@app.route('/')
def welcome():
    return render_template('pizza.html')

