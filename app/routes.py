# imports the Flask object 'flaskApp' from the app package directory.
# note that we don't say 'from app.__init__ import flaskApp', bc __init__ auto-
# matically puts everything inside it to the level of the 'package' (directory)
# that it's in.
from app import flaskApp, db
# imports render_template function
# 'request' used to obtain 'next' in case user is redirected to login after trying to
# access another page.
from flask import render_template, flash, redirect, url_for, request
# imports LoginForm class from forms.py (inside directory 'app')
from app.forms import LoginForm, RegistrationForm
# current_user is the user that's logged in (if applicable), login_u() logs a
# user in. login_required directs user away to page specified in login_view if
# user isn't logged in.
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

# @ statements are decorators: create association btw the event (in this case,
# invocation of the URL '/'  or '/index') and the function index() that follows.
# In general, decorators (ex: @decor(X)) say, "when X happens, call the function
# below me."
@flaskApp.route("/")
@flaskApp.route("/index")
# will redirect to whatever function is passed to login_view if the user is not
# logged in and tries to access index.
@login_required
def index():
    # user = {"username" : "Lydia"} <-- now we have 'real' users in database
    posts = [
    {"author": {"username": "Wood"},
    "body": "This is it."},
    {"author" : {"username" : "Fred"},
    "body" : "The big one."},
    {"author" : {"username" : "George"},
    "body" : "The one we've all been waiting for."}
    ]
    return render_template("index.html", title = "Home Page", posts = posts)

# indicates that this view function accepts get and post requests
# (get is default). GET: request page display. POST: send form data to server.
@flaskApp.route("/login", methods = ["GET", "POST"])
def login():
    # if there is already a user logged in, we shouldn't let them sign in again;
    # if a logged in user tries to go to login page, redirect to index.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    # when user sends POST request (by hitting 'submit'), validate_on_submit
    # gathers all the form data, runs validators, and returns True is everything
    # is right.
    if form.validate_on_submit():
        # query database for entries whose username matches the one on the form.
        # first() returns the first one that matches (use when you know there's
        # only one) (cf. all(), which returns all matching in a list.s)
        user = User.query.filter_by(username = form.username.data).first()
        # if login unsuccessful (user not registered- none- or password wrong.)
        if user is None or not(user.check_password(form.password.data)):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # if login successful, redirect to index
        login_user(user, remember = form.remember_me.data)
        # right after we log the user in, Flask obtains the 'next' argument,
        # which we can query for via request.
        next_page = request.args.get("next")
        # if there is no next page specified (i.e., user wasn't redirected), or
        # the 'next' variable given is not a relative path (i.e., it might be
        # a path to a malicious domain.), redirect to /index by default.
        if not(next_page) or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    # otherwise, show the form.
    return render_template("login.html", title = "Sign In", form = form)

# logs user out if logged in and redirects to index.
@flaskApp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# form class for registration form
@flaskApp.route("/register", methods = ["GET", "POST"])
def register():
    # don't let them register if a user is already signed in.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    # if fields are filled out correctly (and pass our validators; recall that
    # new user's email and username must not already be in database).
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # not in the tutorial, but :)
        flash("Congratulations {}, you are now a registered user!".format(form.username.data))
        return redirect(url_for("login"))
    return render_template("register.html", title = "Register", form = form)
