import os

import jinja2
from flask.views import View


class HTMLView(View):
    methods = ['GET']

    def __init__(self, file_name):
        self.file_name = file_name
        self.html = self.file_name.read_text()
        self.formatted_html = jinja2.Template(self.html)

    def dispatch_request(self):
        return self.formatted_html.render(environ=os.environ, file_name=self.file_name)
