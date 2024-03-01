from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User


@app.route('/')
def welcome():
    return render_template('pizza.html')


@app.route('/register/user', methods = ['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')
    user_id = User.create_user(request.form)
    session['user_id'] = user_id
    return redirect('/')

