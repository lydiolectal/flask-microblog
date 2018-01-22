from flask import render_template
from app import flaskApp, db

# functions to display nice error pages when we get a 404 or 500 error.
@flaskApp.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404

@flaskApp.errorhandler(500)
def internal_error(error):
    # 500 errors can be invoked with a database error. In case some damage was
    # done in this session, rollback() restores db to a clean state.
    db.session.rollback()
    return render_template("500.html"), 500
