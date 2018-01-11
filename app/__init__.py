# import Flask from flask folder
from flask import Flask
from config import Config

# create Flask object called 'app'
flaskApp = Flask(__name__)
# method config.from_object sets configuration variables stored in an object.
flaskApp.config.from_object(Config)

# imports contents of routes module from app folder
# Q? why do we need to specify that it's in the app folder if we are in the app
# folder? doesn't work without the words 'from app'
from app import routes
