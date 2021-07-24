from flask import Response, abort
from flask_login import login_user

from flask_next.request_arg import request_arg
from models import User


@request_arg("username")
def post_login(username):
    user = User.query.filter_by(username=username).first()
    # Login and validate the user.
    # user should be an instance of your `User` class
    if user:
        login_user(user)
        return Response("logged in", 200)
    abort(403)
