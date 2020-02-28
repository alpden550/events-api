from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField
from wtforms.fields.html5 import EmailField


class LoginForm(FlaskForm):
    email = EmailField()
    password = PasswordField()
    is_remembered = BooleanField(label='Запомнить меня')
