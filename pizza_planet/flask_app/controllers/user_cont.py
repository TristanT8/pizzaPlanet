from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user_model import User


@app.route('/')
def welcome():
    return render_template('login_register.html')


@app.route('/register/user', methods = ['POST'])
def register_user():
    if not User.validate_register(request.form):
        return redirect('/')
    user_id = User.create_user(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/user/login', methods = ['POST'])
def login_user():
    if not User.validate_login(request.form):
        return redirect('/')
    email_data = {
        "email" : request.form['email']
    }
    returning_user = User.get_email(email_data)
    session['user_id'] = returning_user.id
    return redirect('/dashboard')


@app.route('/user/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')