import os

from flask import Flask, g
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_next import FlaskNext

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "debug")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "SQLALCHEMY_DATABASE_URI",
    f"""sqlite:///{os.path.join(app.root_path, "test.db")}?check_same_thread=False""",
)
db = SQLAlchemy(app)
CSRFProtect(app)
login_manager = LoginManager(app)
fn = FlaskNext(app)
fn.print()
login_manager.login_view = "routes.login"

from models import User


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    g.user = user
    return user
