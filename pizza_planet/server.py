from flask_app import app
from flask_app.controllers.user_cont import User
from flask_app.controllers.pizza_cont import Pizza
from flask_app.controllers.like_controller import Like


if __name__=="__main__":
    app.run(debug = True)