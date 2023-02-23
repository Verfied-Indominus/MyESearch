import flask_login
from flask_login import LoginManager
from App.models.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)

def logout_user():
    flask_login.logout_user()
