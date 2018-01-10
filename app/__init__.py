# import Flask from flask folder
from flask import Flask

# create Flask object called 'app'
flaskApp = Flask(__name__)

# imports contents of routes module from app folder
# Q? why do we need to specify that it's in the app folder if we are in the app
# folder? doesn't work without the words 'from app'
from app import routes
