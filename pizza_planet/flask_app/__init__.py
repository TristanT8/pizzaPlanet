from flask import Flask, request
app = Flask(__name__)
app.secret_key = "The planet of pizzas"


@app.before_request
def method_override():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method'].upper()
        if method in ['PUT', 'DELETE']:
            request.method = method
            print(f"Overriding method to: {method}")  # Debugging statement
