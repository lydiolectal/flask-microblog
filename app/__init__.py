# import Flask from flask folder
from flask import Flask
from config import Config
# import SQLAlchemy and database migration classes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import flask login extension
from flask_login import LoginManager

# create Flask object called 'app'
flaskApp = Flask(__name__)
# method config.from_object sets configuration variables stored in an object.
flaskApp.config.from_object(Config)
# initialize a database object 'db'
db = SQLAlchemy(flaskApp)
# initialize migration engine as object 'migrate'
migrate = Migrate(flaskApp, db)
# initialize login manager for the flaskApp
login = LoginManager(flaskApp)
# tells login the view function that handles logins; this is useful for redirec-
# ting to the login page if user isn't logged in while trying to view a protect-
# ed page.
login.login_view = "login"

# imports contents of routes module from app folder
# Q? why do we need to specify that it's in the app folder if we are in the app
# folder? doesn't work without the words 'from app'
from app import routes, models
