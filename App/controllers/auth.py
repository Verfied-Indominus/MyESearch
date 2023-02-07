import flask_login
from App.models import User


def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()