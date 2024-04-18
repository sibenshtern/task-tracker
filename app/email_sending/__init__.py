from threading import Thread

from flask import current_app, render_template, url_for
from flask_mail import Message

from app import mail
from app.database.utils import users_utils
from app.database import models


def send_email_by_thread(app, message):
    with app.app_context():
        mail.send(message)


def send_email(
        subject: str,
        sender: str,
        recipients: list,
        text_body: str,
        html_body: str) -> None:
    message = Message(subject, recipients=recipients, sender=sender)
    message.body = text_body
    message.html = html_body

    Thread(
        target=send_email_by_thread,
        args=(current_app._get_current_object(), message)
    ).start()


def send_reset_password_email(user: models.User):
    # Словарь с полезной нагрузкой, который потом зашифруется в
    # Json Web Token
    payloads = {
        "action": "reset_password",
        "user_id": user.id
    }
    token = users_utils.generate_jwt_token(payloads)
    send_email(
        "Сброс пароля",
        sender=current_app.config.get("ADMINS")[0],
        recipients=[user.email],
        text_body=render_template(
            "email/reset_password.txt", user=user, token=token
        ),
        html_body=render_template(
            "email/reset_password.html", user=user, token=token
        )
    )


def send_verification_email(user: models.User) -> None:
    # Словарь с полезной нагрузкой, который потом зашифруется в
    # Json Web Token
    payloads = {
        "action": "verify_account",
        "user_id": user.id
    }
    token = users_utils.generate_jwt_token(payloads)

    send_email(
        "NegotiumTracker",
        sender=current_app.config.get("ADMINS")[0],
        recipients=[user.email],
        text_body="LOL",
        html_body=render_template(
            "email/verify_user.html",
            url=url_for("auth.verify_user", token=token, _external=True),
            user=user
        )
    )
