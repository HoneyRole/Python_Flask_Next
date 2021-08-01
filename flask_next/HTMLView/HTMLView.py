import os

from flask import render_template
from flask.views import View
from flask_login import current_user
from jinja2 import Template

from flask_next.utils import get_g_json


class HTMLView(View):
    methods = ["GET"]

    def __init__(self, file_name):
        self.file_name = file_name
        self.html = self.file_name.read_text()

    def dispatch_request(self):
        t = Template(self.html)
        return render_template(
            "base.html",
            html=t.render(g_json=get_g_json(), current_user=current_user, environ=os.environ),
            environ=os.environ,
            g_json=get_g_json(),
            file_name=self.file_name,
        )
