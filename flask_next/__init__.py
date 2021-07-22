from urllib.parse import quote_plus

from flask import Flask, request, current_app, redirect
from flask_login import current_user, LoginManager

from flask_next.DynamicSetup import DynamicSetup


class FlaskNext:

    def __init__(self, _app: Flask = None):
        self.app = _app
        self._dynamic_setup = DynamicSetup(_app)
        if _app:
            self.init_app(_app)

    def init_app(self, _app):
        self.app = _app
        self._dynamic_setup.app = _app
        self._dynamic_setup.spelunk()

        @self.app.before_request
        def secure_routes():
            if request.endpoint in self._dynamic_setup.secure_routes:
                if not current_user.is_authenticated:
                    return current_app.login_manager.unauthorized()

        @self.app.errorhandler(404)
        def handle_404(e):
            """
            make react routes work by redirecting through /
            in index.html there is a request_path hidden input
            that is read by the react router on init.

            """
            if "/api/" not in request.path and request.method == "GET":
                if 'routes.index' in self._dynamic_setup.public_routes:
                    current_app.logger.warning(f"""{404}, /?request_path={request.path}""")
                    return redirect(f"/?request_path={quote_plus(request.full_path)}")
            return e

    def print(self):
        self._dynamic_setup.print()
