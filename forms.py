from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextField, HiddenField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = TextField("User Name", validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField("Log In")
