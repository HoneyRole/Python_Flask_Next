import os
import random

from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_next import FlaskNext

app = Flask(__name__)
app.config["SECRET_KEY"] = "debug"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"""sqlite:///{os.path.join(app.root_path, "test.db")}?check_same_thread=False"""
db = SQLAlchemy(app)
CSRFProtect(app)
login_manager = LoginManager(app)
fn = FlaskNext(app)
fn.print()
login_manager.login_view = "routes.login"

from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


rand_check_number = random.randint(0, 9999999999)


@app.route("/last_static_update")
def public_last_static_update():
    include_dirs = ["./static/js", "./static/src", "./templates", "./routes"]
    exclude_dir = ["node_modules", "venv", "tmp"]
    notice_exts = ["js", "html", "css"]
    initial_max_age = max_age = float(request.args.get("max_age", -1))
    for include_dir in include_dirs:
        for root, dirs, files in os.walk(include_dir):
            if os.path.basename(root) not in exclude_dir:
                for file in files:
                    if any([file.endswith(ext) for ext in notice_exts]):
                        full_path = os.path.join(root, file)
                        mtime = os.path.getmtime(full_path)
                        if mtime > max_age and initial_max_age != -1:
                            app.logger.debug(
                                "Refresh required because of:{full_path}".format(
                                    full_path=full_path
                                )
                            )
                        max_age = max(max_age, mtime)

    if request.args.get("rand_check_number"):
        if int(request.args.get("rand_check_number")) != rand_check_number:
            app.logger.debug("Refresh required because of:rand_check_number")
    return dict(max_age=max_age, rand_check_number=rand_check_number)
