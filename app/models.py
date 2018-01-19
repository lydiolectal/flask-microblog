from datetime import datetime
# import database object db from the app directory
from app import db
# import login object (login manager)
from app import login
# import hash generator and checker
from werkzeug.security import generate_password_hash, check_password_hash
# mixin is a class in flask-login that includes generic implementations for
# login properties (is_authenticated, is_active, is_anonymous, get_id())
from flask_login import UserMixin
# generate md5 hash for making user avatars
from hashlib import md5

class User(UserMixin, db.Model):
    # primary_key tells db to auto-generate a unique integer for every user
    id = db.Column(db.Integer, primary_key = True)
    # each field is instance of the Column class (takes field type as argument,
    # plus optional arguments such as 'index' and 'unique' that tell db which
    # field are indexed and which are unique, for efficient search.)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    # not a true field; represents the relationship between user and posts.
    # 'Post' indicates the class that is the 'many' side of the relationship.
    # 'author' is the name of a field that will be added to an author's posts
    # that refers back to the user.
    posts = db.relationship("Post", backref = "author", lazy = "dynamic")

    # tells python how to print object of this class
    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # returns avatar for the user, based on a hash of their email.
    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=retro&s={}".format(digest, size)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    # utcnow is the default value of timestamp. The fact that it's indexed
    # allows for retrieval in chronological order.
    # Note: default receives a function, not a return value of function.
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    # references a foreign key, whose value is the id of the User object
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # tells python how to print object of this class
    def __repr__(self):
        return "<Post {}>".format(self.body)

# function that is called when Flask-Login mananger needs to load a new page,
# and needs the user object that is logged in. login calls this with User id.
@login.user_loader
def load_user(id):
    # cast as int bc Flask-Login calls with the id as string.
    return User.query.get(int(id))
