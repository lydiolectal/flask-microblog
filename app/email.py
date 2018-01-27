from flask_mail import Message
from app import mail, flaskApp
from flask import render_template
# python module for running background threads.
from threading import Thread

# sends emails in a background thread started by send_email
def send_async_email(flaskApp, msg):
    # creates an application context
    with flaskApp.app_context():
        mail.send(msg)

# generic function to send email to app users using flask-mail extension.
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(flaskApp, msg)).start()

def send_password_reset_email(user):
    # get the json web token
    token = user.get_reset_password_token()
    # send email with jwt included in the reset URL given in the email.
    send_email("Microblog: Reset Your Password",
        sender = flaskApp.config["ADMINS"][0],
        recipients = [user.email],
        text_body = render_template("email/reset_password.txt",
                                    user = user, token = token),
        html_body = render_template("email/reset_password.html",
                                    user = user, token = token))
