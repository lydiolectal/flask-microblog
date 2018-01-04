# imports the Flask object 'app' from the app package directory
from app import app

# @ statements are decorators: create association btw the event (in this case,
# invocation of the URL '/'  or '/index') and the function index() that follows.
# In general, decorators (ex: @decor(X)) say, "when X happens, call the function
# below me."
@app.route('/')
@app.route('/index')
# a terribly childish test
@app.route('/poop')
def index():
    return "Howdy, Universe!"
