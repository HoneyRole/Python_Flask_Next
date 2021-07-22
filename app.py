from flask import Flask

from flask_next import FlaskNext

app = Flask(__name__)
fn = FlaskNext(app)
fn.print()
app.run()
