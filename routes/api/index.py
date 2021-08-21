from flask import Response
from flask_login import login_user

from flask_next.request_arg import request_arg, get_request_value
from models import User


def post_login():
    username = get_request_value("username")
    user = User.query.filter_by(username=username).first()
    # Login and validate the user.
    # user should be an instance of your `User` class
    if user:
        login_user(user)
        return Response("logged in", 200)
    return Response("Unknown user name", 403)


def post_logout():
    username = get_request_value("username")
    user = User.query.filter_by(username=username).first()
    # Login and validate the user.
    # user should be an instance of your `User` class
    if user:
        login_user(user)
        return Response("logged in", 200)
    return Response("Unknown user name", 403)
