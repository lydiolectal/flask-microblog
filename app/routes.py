# imports the Flask object 'flaskApp' from the app package directory.
# note that we don't say 'from app.__init__ import flaskApp', bc __init__ auto-
# matically puts everything inside it to the level of the 'package' (directory)
# that it's in.
from app import flaskApp, db
# imports render_template function
# 'request' used to obtain 'next' in case user is redirected to login after trying to
# access another page.
from flask import render_template, flash, redirect, url_for, request, g, jsonify
# imports LoginForm class from forms.py (inside directory 'app')
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.forms import ResetPasswordForm, ResetPasswordRequestForm
# current_user is the user that's logged in (if applicable), login_u() logs a
# user in. login_required directs user away to page specified in login_view if
# user isn't logged in.
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from app.email import send_password_reset_email
from werkzeug.urls import url_parse
from datetime import datetime
# translation marker.
from flask_babel import _, get_locale
# detects language, used to detect language of a post.
from guess_language import guess_language
# import translate function from translate.py
from app.translate import translate

# before_request registers the associated function to execute right before a
# view function does. we're using it to record the last time a user was 'seen'.
@flaskApp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    # attaches locale specified by babel to g object.
    g.locale = str(get_locale())

# @ statements are decorators: create association btw the event (in this case,
# invocation of the URL '/'  or '/index') and the function index() that follows.
# In general, decorators (ex: @decor(X)) say, "when X happens, call the function
# below me."
@flaskApp.route("/", methods = ["GET", "POST"])
@flaskApp.route("/index", methods = ["GET", "POST"])
# will redirect to whatever function is passed to login_view if the user is not
# logged in and tries to access index.
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        # if language is unknown, or if the answer is overly complex, assume
        # unspecified language ""
        if language == "UNKNOWN" or len(language) > 5:
            language = ""
        post = Post(body = form.post.data, author = current_user, language = language)
        db.session.add(post)
        db.session.commit()
        flash(_("Your post is now live!"))
        return redirect(url_for("index"))
    # access page # from the query string argument via request.args.get() method.
    # default to 1 if none found.
    page = request.args.get("page", 1, type = int)
    # get a SQL query object for all posts the user is interested in, paginate
    # according to which page we're on and the # of posts per page, as specified
    # by config.
    posts = current_user.followed_posts().paginate(page,
        flaskApp.config["POSTS_PER_PAGE"], False)
    # set the URL for the 'next' and 'previous buttons'
    next_url = url_for("index", page = posts.next_num) if posts.has_next else None
    prev_url = url_for("index", page = posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title = _("Home Page"), form = form,
        posts = posts.items, next_url = next_url, prev_url = prev_url)

@flaskApp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type = int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,
        flaskApp.config["POSTS_PER_PAGE"], False)
    next_url = url_for("explore", page = posts.next_num) if posts.has_next else None
    prev_url = url_for("explore", page = posts.prev_num) if posts.has_prev else None
    # reuse the index template, since the basic layout is the same.
    return render_template("index.html", title = _("Explore"), posts = posts.items,
        next_url = next_url, prev_url = prev_url)

# indicates that this view function accepts get and post requests
# (get is default). GET: request page display. POST: send form data to server.
@flaskApp.route("/login", methods = ["GET", "POST"])
def login():
    # if there is already a user logged in, we shouldn't let them sign in again;
    # if a logged in user tries to go to login page, redirect to index.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    # when user sends POST request (by hitting 'submit'), validate_on_submit
    # gathers all the form data, runs validators, and returns True is everything
    # is right.
    if form.validate_on_submit():
        # query database for entries whose username matches the one on the form.
        # first() returns the first one that matches (use when you know there's
        # only one) (cf. all(), which returns all matching in a list.s)
        user = User.query.filter_by(username = form.username.data).first()
        # if login unsuccessful (user not registered- none- or password wrong.)
        if user is None or not(user.check_password(form.password.data)):
            flash(_("Invalid username or password"))
            return redirect(url_for("login"))
        # if login successful, redirect to index
        login_user(user, remember = form.remember_me.data)
        # right after we log the user in, Flask obtains the 'next' argument,
        # which we can query for via request.
        next_page = request.args.get("next")
        # if there is no next page specified (i.e., user wasn't redirected), or
        # the 'next' variable given is not a relative path (i.e., it might be
        # a path to a malicious domain.), redirect to /index by default.
        if not(next_page) or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    # otherwise, show the form.
    return render_template("login.html", title = _("Sign In"), form = form)

# logs user out if logged in and redirects to index.
@flaskApp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

# form page for registration form
@flaskApp.route("/register", methods = ["GET", "POST"])
def register():
    # don't let them register if a user is already signed in.
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    # if fields are filled out correctly (and pass our validators; recall that
    # new user's email and username must not already be in database).
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # not in the tutorial, but :)
        # annoying babel string substitution syntax is based on Python 2.
        flash(_("Congratulations %(username)s, you are now a registered user!", username = form.username.data))
        return redirect(url_for("login"))
    return render_template("register.html", title = _("Register"), form = form)

# profile page that only shows if there is a user logged in.
# the value of 'username' inside the decorator <> and the parameter is passed in
# by jinja2 in user.html, which sets username to current_user.username
@flaskApp.route("/user/<username>")
@login_required
def user(username):
    # tries to look up user by username; 404 error if lookup fails.
    user = User.query.filter_by(username = username).first_or_404()
    page = request.args.get("page", 1, type = int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page,
        flaskApp.config["POSTS_PER_PAGE"], False)
    next_url = url_for("user", page = posts.next_num, username = username) if posts.has_next else None
    prev_url = url_for("user", page = posts.prev_num, username = username) if posts.has_prev else None
    return render_template("user.html", user = user, posts = posts.items,
        next_url = next_url, prev_url = prev_url)

@flaskApp.route("/edit_profile", methods = ["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    # if profile is edited without any errors, submit and save to db.
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_("Your changes have been saved."))
        return redirect(url_for("edit_profile"))
    # if the user has just navigated to this page ("GET" request), display it
    # with the user's data in its current state (i.e., this "prefills" form).
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    # if the user tried to submit ("POST"), but there were errors, display a
    # blank profile editor page.
    return render_template("edit_profile.html", title = _("Edit Profile"), form = form)

@flaskApp.route("/follow/<username>")
@login_required
def follow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash(_("User %(username)s not found.", username = username))
        return redirect(url_for("index"))
    if user == current_user:
        flash(_("You cannot follow yourself."))
        return redirect(url_for("user", username = username))
    current_user.follow(user)
    db.session.commit()
    flash(_("You are following %(username)s!", username = username))
    return redirect(url_for("user", username = username))

@flaskApp.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        flash(_("User %(username)s not found.", username = username))
        return redirect(url_for("index"))
    if user == current_user:
        flash(_("You cannot unfollow yourself."))
        return redirect(url_for("user", username = username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_("You are no longer following %(username)s.", username = username))
    return redirect(url_for("user", username = username))

# request page for resetting password
@flaskApp.route("/reset_password_request", methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            send_password_reset_email(user)
        # flash regardless of whether user is actually in the system;
        # this prevents clients from figuring out whether a given user is
        # registered or not.
        flash(_("Please check your email for instructions to reset your password."))
        return redirect(url_for("login"))
    return render_template("reset_password_request.html",
        title = _("Request Password Reset"), form = form)

# password reset page
@flaskApp.route("/reset_password/<token>", methods = ["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("index"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_("Password has been successfully reset."))
        return redirect(url_for("login"))
    return render_template("reset_password.html", form = form)

@flaskApp.route("/translate", methods=["POST"])
@login_required
def translate_text():
    # request.form is a dictionary that flask exposes with the data incl. in
    # the request submission.
    # We pass in these 3 values (text, sourcelang, destlang) to translate,
    # which returns the translated string. We pass this string in as the value
    # in a dictionary, which jsonify converts into JSON formatted payload for
    # the client.
    return jsonify({"text": translate(request.form["text"],
                                    request.form["source_language"],
                                    request.form["dest_language"])})
