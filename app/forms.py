from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# inheriting FlaskForm class
# class represents a form within our application.
# each field (username, etc) is a class variable.
class LoginForm(FlaskForm):
    # each field is an object of its own, stored as a class variable.
    # first arg is its label. validators=[Datareqd] just makes sure the fields
    # are filled in.
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
