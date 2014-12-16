__author__ = 'janiniem'

from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, IntegerField
from wtforms.validators import Required, Email


class LoginForm(Form):
    login_name = TextField('Login', [Required()])
    password = PasswordField('Password', [Required()])


class MonkeyForm(Form):
    email = TextField('Email', validators=[Required(), Email(message=u'Invalid email address.')])
    name = TextField('Name', validators=[Required()])
    age = IntegerField('Age', validators=[Required()])
    password = PasswordField('Password')