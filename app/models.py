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

    # tells python how to print object of this class
    def __repr__(self):
        return "<User {}>".format(self.username)
