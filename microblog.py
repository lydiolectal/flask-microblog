# imports the Flask application instance 'flaskApp' from the package
# (our directory) named 'app'
from app import flaskApp, db, cli
from app.models import User, Post

@flaskApp.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}
