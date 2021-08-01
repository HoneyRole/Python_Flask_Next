import os
from pathlib import Path
from random import randint
from urllib.parse import quote_plus

from flask import Flask, request, current_app, redirect, g
from flask_login import current_user

from flask_next.DynamicSetup import DynamicSetup
from flask_next.d_serialize import d_serialize
from flask_next.utils import get_g_json


class FlaskNext:
    rand_check_number = randint(0, 9999999999)

    def __init__(self, _app: Flask = None):
        self.app = _app
        self._dynamic_setup = DynamicSetup(_app)
        if _app:
            self.init_app(_app)

    def init_app(self, _app, _routes_path:Path="./routes"):
        self.app = _app
        self._dynamic_setup.app = _app
        self._dynamic_setup.spelunk(_routes_path)

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
                if "routes.index.html" in self._dynamic_setup.public_routes:
                    current_app.logger.warning(
                        f"""{404}, /?request_path={request.path}"""
                    )
                    return redirect(f"/?request_path={quote_plus(request.full_path)}")
            return e

        @self.app.route('/g')
        def route_get_g_json():
            return get_g_json()

        @self.app.route("/last_static_update")
        def public_last_static_update():
            include_dirs = ["./static/js", "./static/src", "./templates", "./routes"]
            notice_exts = ["js", "html", "css"]
            initial_max_age = max_age = float(request.args.get("max_age", -1))
            for include_dir in include_dirs:
                for root, dirs, files in os.walk(include_dir):
                    for file in files:
                        if any([file.endswith(ext) for ext in notice_exts]):
                            full_path = os.path.join(root, file)
                            mtime = os.path.getmtime(full_path)
                            if mtime > max_age and initial_max_age != -1:
                                self.app.logger.debug(
                                    "Refresh required because of:{full_path}".format(
                                        full_path=full_path
                                    )
                                )
                            max_age = max(max_age, mtime)

            if request.args.get("rand_check_number"):
                if int(request.args.get("rand_check_number")) != self.rand_check_number:
                    self.app.logger.debug(
                        "Refresh required because of:rand_check_number"
                    )
            return dict(max_age=max_age, rand_check_number=self.rand_check_number)

    def print(self):
        self._dynamic_setup.print()
