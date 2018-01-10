# imports the Flask object 'app' from the app package directory
from app import flaskApp
# imports render_template function
from flask import render_template

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
