from flask import Blueprint
from flask import render_template, flash, request

from flask_login import login_user, logout_user, current_user

from werkzeug.utils import redirect

from . import forms
from app.database.utils import users_utils, session
from app import email


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect('/main_app')

    form = forms.LoginForm()

    if form.validate_on_submit():
        user = users_utils.get_user(email=form.email.data.strip())
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/main_app/all')

        return render_template(
            'auth/login.html', form=form,
            message="Неправильный логин или пароль. Повторите попытку"
        )

    return render_template('auth/login.html', form=form, message=None)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if current_user.is_authenticated:
        return redirect('/main_app')

    form = forms.SignupForm()

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'auth/signup.html', form=form, title='Регистрация'
            )
        if users_utils.get_user(email=form.email.data) is not None:
            return render_template(
                'auth/signup.html', form=form, title='Регистрация',
                message="Пользователь с такой почтой уже зарегистрирован. "
                        "Повторите попытку"
            )

        user = users_utils.create_user(
            form.email.data, form.name.data, form.password.data
        )
        email.send_verification_email(user)

        return redirect('/login')

    return render_template('auth/signup.html', form=form, message=None)


@blueprint.route('/verify_user', methods=["GET", "POST"])
def verify_user():
    token = request.args.get("token")
    if token is not None:
        user = users_utils.verify_jwt_token(token)

        if user is None:
            return redirect("/")

        user.verify()
        session.commit()
        return redirect('/main_app/apikey')
    else:
        form = forms.MailRequestForm()

        if form.validate_on_submit():
            user = users_utils.get_user(email=form.email.data)
            if user is not None:
                email.send_verification_email(user)

            if current_user.is_authenticated:
                return redirect('/main_app')

            return redirect('/login')

        params = {"form": form, "title": "Верификация"}
        form.submit.label.text = "Верификация"

        return render_template("auth/mail_request.html", **params)


@blueprint.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect('/main_app')

    token = request.args.get("token")
    if token is not None:
        user = users_utils.verify_jwt_token(token)

        if user is None:
            return redirect('/')

        form = forms.ResetPasswordForm()

        if form.validate_on_submit():
            user.set_password(form.new_password.data)
            session.commit()

            return redirect('/login')

        return render_template('auth/reset_password.html', form=form)
    else:
        form = forms.MailRequestForm()

        if form.validate_on_submit():
            user = users_utils.get_user(email=form.email.data)
            if user is not None:
                email.send_reset_password_email(user)

            return redirect('/login')

        form.submit.label.text = "Сбросить пароль"
        params = {"form": form, "title": "Сбросить пароль"}
        return render_template("auth/mail_request.html", **params)
