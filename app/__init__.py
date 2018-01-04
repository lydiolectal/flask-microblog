# import flask package as a Flask object
from flask import Flask

# create instance of Flask object called 'app'
app = Flask(__name__)

# imports route class from routes.py, which is contained in the package folder
# 'app' -- note that this 'app' is different from the 'app' above, which is a
# Flask object.
from app import routes
