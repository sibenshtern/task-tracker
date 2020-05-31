from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail
from app.database.utils import users_utils


def send_email_by_thread(app, message):
    with app.app_context():
        mail.send(message)


def send_email(subject, sender, recipients, text_body, html_body):
    message = Message(subject, recipients=recipients, sender=sender)
    message.body = text_body
    message.html = html_body

    Thread(
        target=send_email_by_thread,
        args=(current_app._get_current_object(), message)
    ).start()


def send_reset_password_email(user):
    payloads = {
        "action": "reset_password",
        "user_id": user.id
    }
    token = users_utils.generate_jwt_token(payloads)
    send_email(
        "NegotiumTracker",
        sender=current_app.config.get("ADMINS")[0],
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password.txt", user=user, token=token
        ),
        html_body=render_template(
            "email/reset_password.html", user=user, token=token
        )
    )
