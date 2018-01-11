# imports the Flask object 'flaskApp' from the app package directory.
# note that we don't say 'from app.__init__ import flaskApp', bc __init__ auto-
# matically puts everything inside it to the level of the 'package' (directory)
# that it's in.
from app import flaskApp
# imports render_template function
from flask import render_template
# imports LoginForm class from forms.py (inside directory 'app')
from app.forms import LoginForm

# @ statements are decorators: create association btw the event (in this case,
# invocation of the URL '/'  or '/index') and the function index() that follows.
# In general, decorators (ex: @decor(X)) say, "when X happens, call the function
# below me."
@flaskApp.route('/')
@flaskApp.route('/index')
# a terribly childish test
@flaskApp.route('/poop')
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

@flaskApp.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", title = "Sign In", form = form)
