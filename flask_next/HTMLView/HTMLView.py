import json
import os

from flask import render_template, g
from flask.views import View
from flask_login import current_user
from jinja2 import FileSystemLoader, Environment, PackageLoader, Template

from flask_next.d_serialize import d_serialize


class HTMLView(View):
    methods = ["GET"]

    def __init__(self, file_name):
        self.file_name = file_name
        self.html = self.file_name.read_text()

    def dispatch_request(self):
        t = Template(self.html)
        g_json = d_serialize(g)
        g_json["user"] = d_serialize(current_user)
        return render_template(
            "base.html",
            html=t.render(g_json=g_json, current_user=current_user, environ=os.environ),
            environ=os.environ,
            g_json=g_json,
            file_name=self.file_name,
        )
