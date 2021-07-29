import os

from flask import Flask, g
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_next import FlaskNext

db = SQLAlchemy()
csrf = CSRFProtect()
fn = FlaskNext()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    """
    create a flask app

    :return:
    """
    _app = Flask(__name__)
    _app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "debug")
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    _app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"""sqlite:///{os.path.join(_app.root_path, "test.db")}?check_same_thread=False""",
    )
    fn.init_app(_app)
    db.init_app(_app)
    migrate.init_app(_app, db)
    csrf.init_app(_app)
    login_manager.init_app(_app)
    login_manager.login_view = "routes.index.get_post_login"

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.get(user_id)
        g.user = user
        return user

    return _app


if __name__ == "__main__":
    app = create_app()
    app.run()
