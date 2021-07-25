import os

import flask
from flask_login import login_user

from models import User
from forms import LoginForm


def get_post_login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # Login and validate the user.
        # user should be an instance of your `User` class
        if user:
            login_user(user)

            flask.flash("Logged in successfully.")

            return flask.redirect("/")
        flask.flash("user not found")
    flask.flash(",".join(error for error in form.errors))
    return flask.render_template("login_page.html", environ=os.environ, form=form)
