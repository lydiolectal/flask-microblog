from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

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

# form for registering new user
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    # email() validator comes with WTForms, ensures that it is in email format.
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    # makes user type password 2x, then checks that they match.
    password2 = PasswordField("Password", validators=[DataRequired(),
        EqualTo("password")])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Register")

    # WTForms allows custom validators in the form validate_<fieldname>().
    # validate_username and _email check that there are no preexisting users
    # that have the same name/email in the db.
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        email = User.query.filter_by(username = email.data).first()
        if email is not None:
            raise ValidationError("Please use a different email.")
