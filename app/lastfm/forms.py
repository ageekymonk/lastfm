from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    id = StringField('ID', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])