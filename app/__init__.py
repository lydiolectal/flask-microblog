import os
# import logging package for logging errors
import logging

# import Flask from flask folder
from flask import Flask
from config import Config

# import SQLAlchemy and database migration classes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# import flask login extension
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
# mail, bootstrap extensions
from flask_mail import Mail
from flask_bootstrap import Bootstrap
# datetime conversion and formatting library
from flask_moment import Moment

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
# create a mail object that can send emails to users.
mail = Mail(flaskApp)
# create a bootstrap object that renders html templates
bootstrap = Bootstrap(flaskApp)
# initialize moment object
moment = Moment(flaskApp)

# imports contents of routes module from app folder
# Q? why do we need to specify that it's in the app folder if we are in the app
# folder? doesn't work without the words 'from app'
from app import routes, models, errors

# if the app is *not* in debug mode
if not flaskApp.debug:

    # create email handler, then attach to app.logger to send emails in case of
    # errors.
    if flaskApp.config["MAIL_SERVER"]:
        auth = None
        if flaskApp.config["MAIL_USERNAME"] or flaskApp.config["MAIL_PASSWORD"]:
            auth = (flaskApp.config["MAIL_USERNAME"], flaskApp.config["MAIL_PASSWORD"])
        secure = None
        if flaskApp.config["MAIL_USE_TLS"]:
            secure = ()
        # SMTP handler instance.
        mail_handler = SMTPHandler(
            mailhost = (flaskApp.config["MAIL_SERVER"], flaskApp.config["MAIL_PORT"]),
            fromaddr = "no-reply@" + flaskApp.config["MAIL_SERVER"],
            toaddrs = flaskApp.config["ADMINS"], subject = "Microblog Failure",
            credentials = auth, secure = secure)
        # set level so that the handler only reports errors, not warnings, etc.
        mail_handler.setLevel(logging.ERROR)
        # attach handler to app.logger object.
        flaskApp.logger.addHandler(mail_handler)

    # log to a file in case of errors.
    if not os.path.exists("logs"):
        os.mkdir("logs")
    # instantiate a file handler whose path is logs/microblog.log, whose max
    # file size is 10kb, and who only keeps 10 log items at a time.
    file_handler = RotatingFileHandler("logs/microblog.log", maxBytes = 10240,
        backupCount = 10)
    # not sure why this is using python2 string formatting syntax. does
    # setFormatter still take python2 string template?
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
    # set level so that handler writes to file for all levels above 'info'
    file_handler.setLevel(logging.INFO)
    flaskApp.logger.addHandler(file_handler)

    # lower level for logger in general.
    flaskApp.logger.setLevel(logging.INFO)
    # this is the default message whenever an 'info' level event happens.
    flaskApp.logger.info("Microblog startup")
