import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY is an important configuration item in most Flask apps;
    # Flask uses it as a crytographic key.
    # 'or': generate a key from the operating environment 'os.environ'
    # (also called "SECRET_KEY"). If not available, use the hardcoded string.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # set the path for flaskApp's database.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # configure flask to send emails in case of errors.
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["lydiding@gmail.com"]

    # set number of posts allowed per page for pagination.
    POSTS_PER_PAGE = 3

    # specifies which languages are supported for this app.
    LANGUAGES = ["en", "es"]
    
    # gets key for translation API.
    MS_TRANSLATOR_KEY = os.environ.get["MS_TRANSLATOR_KEY"]
