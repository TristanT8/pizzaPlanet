from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.pizza_model import Pizza
from flask_app.models.user_model import User


@app.route('/dashboard')
def pizza_home():
    if "user_id" not in session:
        return redirect('/')
    user = User.one_user({"id" : session['user_id']})
    return render_template('index.html', user = user, pizza = Pizza.get_all_pizzas())


@app.route('/new/pizza')
def new_pizza():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new_pizza.html')


@app.route('/validate/pizza', methods = ['POST'])
def validate_pizza():
    if 'user_id' not in session:
        return redirect('/')
    if not Pizza.validate_pizza(request.form):
        return redirect('/new/pizza')

    data = {
        "user_id" : session['user_id'],
        "baker" : request.form['baker'],
        "dough" : request.form['dough'],
        "sauce_base" : request.form['sauce_base'],
        "meat" : request.form['meat'],
        "toppings" : request.form['toppings']
    }

    Pizza.create_pizza(data)
    return redirect('/dashboard')

