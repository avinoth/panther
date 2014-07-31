from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    name = TextField('name', validators = [Required()])
    email = TextField('email', validators = [Required()])
    password = PasswordField('password', validators = [Required()])