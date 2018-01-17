# imports the Flask object 'flaskApp' from the app package directory.
# note that we don't say 'from app.__init__ import flaskApp', bc __init__ auto-
# matically puts everything inside it to the level of the 'package' (directory)
# that it's in.
from app import flaskApp
# imports render_template function
from flask import render_template, flash, redirect, url_for
# imports LoginForm class from forms.py (inside directory 'app')
from app.forms import LoginForm

# @ statements are decorators: create association btw the event (in this case,
# invocation of the URL '/'  or '/index') and the function index() that follows.
# In general, decorators (ex: @decor(X)) say, "when X happens, call the function
# below me."
@flaskApp.route("/")
@flaskApp.route("/index")
def index():
    user = {"username" : "Lydia"}
    posts = [
    {"author": {"username": "Wood"},
    "body": "This is it."},
    {"author" : {"username" : "Fred"},
    "body" : "The big one."},
    {"author" : {"username" : "George"},
    "body" : "The one we've all been waiting for."}
    ]
    return render_template("index.html", title = "Home", user = user, posts = posts)

# indicates that this view function accepts get and post requests
# (get is default). GET: request page display. POST: send form data to server.
@flaskApp.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    # when user sends POST request (by hitting 'submit'), validate_on_submit
    # gathers all the form data, runs validators, and returns True is everything
    # is right.
    if form.validate_on_submit():
        # flash returns a message that is meant to be displayed
        flash("Login requested for user {}, remember_me = {}".format(
        form.username.data, form.remember_me.data))
        # if login successful, redirect to index (this activates index() f'n.)
        return redirect(url_for("index"))
    # otherwise, show the form.
    return render_template("login.html", title = "Sign In", form = form)
