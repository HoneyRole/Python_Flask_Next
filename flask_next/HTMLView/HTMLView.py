import os

from flask import render_template
from flask.views import View
from jinja2 import FileSystemLoader, Environment, PackageLoader


class HTMLView(View):
    methods = ["GET"]

    def __init__(self, file_name):
        self.file_name = file_name
        self.html = self.file_name.read_text()

    def dispatch_request(self):
        return render_template(
            "base.html", html=self.html, environ=os.environ, file_name=self.file_name
        )
