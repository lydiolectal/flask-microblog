from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User
# lazy_gettext delays evaluation of the text until it gets used.
from flask_babel import _, lazy_gettext as _l

# pass in current_user; req'd for my solution to the username problem.
# from flask_login import current_user

# inheriting FlaskForm class
# class represents a form within our application.
# each field (username, etc) is a class variable.
class LoginForm(FlaskForm):
    # each field is an object of its own, stored as a class variable.
    # first arg is its label. validators=[Datareqd] just makes sure the fields
    # are filled in.
    username = StringField(_l("Username"), validators=[DataRequired()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Sign In"))

# form for registering new user
class RegistrationForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    # email() validator comes with WTForms, ensures that it is in email format.
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    # makes user type password 2x, then checks that they match.
    password2 = PasswordField(_l("Re-type Password"), validators=[DataRequired(),
        EqualTo("password")])
    remember_me = BooleanField(_l("Remember Me"))
    submit = SubmitField(_l("Register"))

    # WTForms allows custom validators in the form validate_<fieldname>().
    # validate_username and _email check that there are no preexisting users
    # that have the same name/email in the db.
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError(_("Please use a different username."))

    def validate_email(self, email):
        email = User.query.filter_by(username = email.data).first()
        if email is not None:
            raise ValidationError(_("Please use a different email."))

# class for profile editor form.
class EditProfileForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired()])
    about_me = TextAreaField(_l("About Me"), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l("Submit"))

    # author's way: pass current_user's username in as instance variable.
    def __init__(self, original_username, *args, **kwargs):
        # instantiate parent classes
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = username.data).first()
            if user is not None:
                raise ValidationError(_("Please use a different username."))

    # my way: import current_user into this file, then check their name against
    # the name in the username field.
    # def validate_username(self, username):
    #     if username.data != current_user.username:
    #         user = User.query.filter_by(username = username.data).first()
    #         # if the user is in the db
    #         if user is not None:
    #             raise ValidationError("Please use a different username.")

# class for post editor form
class PostForm(FlaskForm):
    post = TextAreaField(_l("Say something"), validators=[DataRequired(),
        Length(min=0, max=140)])
    submit = SubmitField(_l("Submit"))

# class for password reset request
class ResetPasswordRequestForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email()])
    submit = SubmitField(_l("Request Password Reset"))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("Password"), validators=[DataRequired()])
    password2 = PasswordField(_l("Re-type Password"), validators=[DataRequired(),
        EqualTo("password")])
    submit = SubmitField(_l("Reset Password"))
