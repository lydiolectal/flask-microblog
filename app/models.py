from datetime import datetime
# import database object db from the app directory
# import login object (login manager)
from app import db, login, flaskApp
# import hash generator and checker
from werkzeug.security import generate_password_hash, check_password_hash
# mixin is a class in flask-login that includes generic implementations for
# login properties (is_authenticated, is_active, is_anonymous, get_id())
from flask_login import UserMixin
# generate md5 hash for making user avatars
from hashlib import md5
# import time and json web tokens package.
from time import time
import jwt

# an association table that represents a 'follow' relationship between 2 users.
followers = db.Table("followers",
db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
db.Column("followed_id", db.Integer, db.ForeignKey("user.id")))

class User(UserMixin, db.Model):
    # primary_key tells db to auto-generate a unique integer for every user
    id = db.Column(db.Integer, primary_key = True)
    # each field is instance of the Column class (takes field type as argument,
    # plus optional arguments such as 'index' and 'unique' that tell db which
    # field are indexed and which are unique, for efficient search.)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    # not a true field; represents the" relationship between user and posts.
    # 'Post' indicates the class that is the 'many' side of the relationship.
    # 'author' is the name of a field that will be added to an author's posts
    # that refers back to the user.
    posts = db.relationship("Post", backref = "author", lazy = "dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    # follow relationship from the side of the follower. 'followed' relationship
    # links the user to the people that she follows; backref links user to the
    # other users that follow her.
    followed = db.relationship("User", secondary = followers,
    primaryjoin = (followers.c.follower_id == id),
    secondaryjoin = (followers.c.followed_id == id),
    backref = db.backref("followers", lazy = "dynamic"), lazy = "dynamic")

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

    # follow, unfollow, and ascertain whether current user is following someone.
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        # among the follow relationships that have 'self' as the follower,
        # return the number that have 'user' as the followee.
        return self.followed.filter(followers.c.followed_id==user.id).count()>0

    # return the posts written by people that this user is following.
    def followed_posts(self):
        # posts by people this user is following.
        followed = Post.query.join(followers,(
            followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        # combine with own posts, then return.
        own = Post.query.filter(Post.user_id == self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    # generates a json web token as a string (decode changes byte to string).
    # set default expiry time to 10 minutes.
    def get_reset_password_token(self, expires_in = 600):
        return jwt.encode({"reset_password": self.id, "exp": time()+expires_in},
            flaskApp.config["SECRET_KEY"], algorithm = "HS256").decode("utf-8")

    # static methods are invoked w/ the class name, not the instance. Ex:
    # User.verify_reset_password_token, not some_user.verify_reset_password...
    # this method returns the id of the user, given the json web token.
    @staticmethod
    def verify_reset_password_token(token):
        try:
            # get the value of "reset_password" from payload.
            id = jwt.decode(token, flaskApp.config["SECRET_KEY"],
                algorithm = "HS256")["reset_password"]
        except:
            # jwt.decode() will throw an exception if token cannot be validated.
            # we return None in this case.
            return
        return User.query.get(id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    # utcnow is the default value of timestamp. The fact that it's indexed
    # allows for retrieval in chronological order.
    # Note: default receives a function, not a return value of function.
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    # references a foreign key, whose value is the id of the User object
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # stores language detected for the post.
    language = db.Column(db.String(5))

    # tells python how to print object of this class
    def __repr__(self):
        return "<Post {}>".format(self.body)

# function that is called when Flask-Login mananger needs to load a new page,
# and needs the user object that is logged in. login calls this with User id.
@login.user_loader
def load_user(id):
    # cast as int bc Flask-Login calls with the id as string.
    return User.query.get(int(id))
