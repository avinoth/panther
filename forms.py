from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import Required

class PostForm(Form):
    title = TextField('title', validators = [Required()])
    body = TextAreaField('body', validators = [Required()])
    