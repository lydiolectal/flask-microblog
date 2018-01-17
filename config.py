import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # SECRET_KEY is an important configuration item in most Flask apps;
    # Flask uses it as a crytographic key.
    # 'or': generate a key from the operating environment 'os.environ'
    # (also called "SECRET_KEY"). If not available, use the hardcoded string.
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
