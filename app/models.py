from datetime import datetime
# import database object db from the app directory
from app import db

class User(db.Model):
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
