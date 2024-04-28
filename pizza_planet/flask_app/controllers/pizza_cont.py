from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.pizza_model import Pizza
from flask_app.models.user_model import User
from flask_app.models.like_model import Like
from flask_app.models.comment_model import Comment

@app.route('/dashboard')
def pizza_home():
    if "user_id" not in session:
        return redirect('/')
    
    user_id = session['user_id']
    user = User.one_user({"id": user_id})
    pizzas = Pizza.get_all_pizzas()

    # Loop through pizzas to determine if the user liked each pizza
    for pizza in pizzas:
        # Check if the current user liked this pizza
        liked_by_user = Like.has_liked(user_id, pizza.id)
        pizza.liked_by_user = bool(liked_by_user)  # Convert to boolean
        
        # Debugging output
        print(f"User {user_id} liked Pizza {pizza.id}: {pizza.liked_by_user}")

    return render_template('home_page.html', user=user, pizzas=pizzas)


@app.route('/new/pizza')
def new_pizza():
    if "user_id" not in session:
        return redirect('/')
    return render_template('new_pizza.html')


@app.route('/validate/pizza', methods=['POST'])
def validate_pizza():
    if 'user_id' not in session:
        return redirect('/')
    
    # Print request form data
    print(request.form)

    # Check if pizza data validation passes
    if not Pizza.validate_pizza(request.form):
        return redirect('/new/pizza')
    
    selected_sauce = ', '.join(request.form.getlist('sauce_base'))
    selected_cheese = ', '.join(request.form.getlist('cheese'))
    selected_meat = ', '.join(request.form.getlist('meat'))
    selected_vegetables = ', '.join(request.form.getlist('vegetables'))
    print(selected_sauce, selected_cheese, selected_meat, selected_vegetables)

    data = {
        "user_id": session['user_id'],
        "baker": request.form['baker'],
        "dough": request.form['dough'],
        "sauce_base": selected_sauce,
        "cheese": selected_cheese,
        "meat": selected_meat,
        "vegetables": selected_vegetables
    }

    print(data)  # Check the final data before inserting into the database

    Pizza.create_pizza(data)
    return redirect('/dashboard')


@app.route('/pizza/<int:pizza_id>')
def view_pizza(pizza_id):
    if 'user_id' not in session:
        return redirect('/')
    pizza = Pizza.get_pizza({'id': pizza_id})
    if not pizza:
        flash("Pizza not found.", "error")
        return redirect('/')

    comments = Comment.get_comments_by_pizza_id(pizza_id)
    return render_template('view_pizza.html', pizza=pizza, comments=comments)


@app.route('/edit/pizza/<int:id>')
def edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/')
    pizza = Pizza.get_pizza({'id' : id})
    return render_template('edit_pizza.html', pizza = pizza)


@app.route('/post/edit/pizza/<int:id>', methods=['POST'])
def post_edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/')

    # Check if pizza data validation passes
    if not Pizza.validate_pizza(request.form):
        flash('Invalid pizza data. Please check your inputs.', 'error')
        return redirect(f'/edit/pizza/{id}')

    data = {
        'id': id,
        "baker": request.form['baker'],
        "dough": request.form['dough'],
        "sauce_base": ', '.join(request.form.getlist('sauce_base')),
        "cheese": ', '.join(request.form.getlist('cheese')),
        "meat": ', '.join(request.form.getlist('meat')),
        "vegetables": ', '.join(request.form.getlist('vegetables'))
    }

    Pizza.update_pizza(data)
    return redirect('/dashboard')


@app.route('/pizza/delete/<int:id>')
def delete_pizza(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Pizza.delete_pizza({'id' : id})
    return redirect('/dashboard')


@app.route('/post/edit/pizza/<int:id>', methods=['POST'])
def post_edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/')

    # Check if pizza data validation passes
    if not Pizza.validate_pizza(request.form):
        flash('Invalid pizza data. Please check your inputs.', 'error')
        return redirect(f'/edit/pizza/{id}')

    data = {
        'id': id,
        "baker": request.form['baker'],
        "dough": request.form['dough'],
        "sauce_base": ', '.join(request.form.getlist('sauce_base')),
        "cheese": ', '.join(request.form.getlist('cheese')),
        "meat": ', '.join(request.form.getlist('meat')),
        "vegetables": ', '.join(request.form.getlist('vegetables'))
    }

    Pizza.update_pizza(data)
    return redirect('/dashboard')


@app.route('/pizza/delete/<int:id>')
def delete_pizza(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Pizza.delete_pizza({'id' : id})
    return redirect('/dashboard')

@app.route('/post/edit/pizza/<int:id>', methods=['POST'])
def post_edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/')

    # Check if pizza data validation passes
    if not Pizza.validate_pizza(request.form):
        flash('Invalid pizza data. Please check your inputs.', 'error')
        return redirect(f'/edit/pizza/{id}')

    data = {
        'id': id,
        "baker": request.form['baker'],
        "dough": request.form['dough'],
        "sauce_base": ', '.join(request.form.getlist('sauce_base')),
        "cheese": ', '.join(request.form.getlist('cheese')),
        "meat": ', '.join(request.form.getlist('meat')),
        "vegetables": ', '.join(request.form.getlist('vegetables'))
    }

    Pizza.update_pizza(data)
    return redirect('/dashboard')


@app.route('/pizza/delete/<int:id>')
def delete_pizza(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Pizza.delete_pizza({'id' : id})
    return redirect('/dashboard')
@app.route('/post/edit/pizza/<int:id>', methods=['POST'])
def post_edit_pizza(id):
    if 'user_id' not in session:
        return redirect('/')

    # Check if pizza data validation passes
    if not Pizza.validate_pizza(request.form):
        flash('Invalid pizza data. Please check your inputs.', 'error')
        return redirect(f'/edit/pizza/{id}')

    data = {
        'id': id,
        "baker": request.form['baker'],
        "dough": request.form['dough'],
        "sauce_base": ', '.join(request.form.getlist('sauce_base')),
        "cheese": ', '.join(request.form.getlist('cheese')),
        "meat": ', '.join(request.form.getlist('meat')),
        "vegetables": ', '.join(request.form.getlist('vegetables'))
    }

    Pizza.update_pizza(data)
    return redirect('/dashboard')


@app.route('/pizza/delete/<int:id>')
def delete_pizza(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    Pizza.delete_pizza({'id' : id})
    return redirect('/dashboard')

