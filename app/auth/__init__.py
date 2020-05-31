from flask import Blueprint
from flask import render_template, flash, request

from flask_login import login_user, logout_user, current_user

from werkzeug.utils import redirect

from . import forms, email
from app.database.utils import users_utils, session


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect('/app')

    form = forms.LoginForm()

    if form.validate_on_submit():
        user = users_utils.get_user(email=form.email.data.strip())
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/app/all')

        return render_template(
            'auth/login.html', form=form,
            message="Неправильный логин или пароль. Повторите попытку"
        )

    return render_template('auth/login.html', form=form, message=None)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if current_user.is_authenticated:
        return redirect('/app')

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

        users_utils.create_user(
            form.email.data, form.name.data, form.password.data
        )

        return redirect('/login')

    return render_template('auth/signup.html', form=form, message=None)


@blueprint.route('/reset_password', methods=["GET", "POST"])
def reset_password():
    if current_user.is_authenticated:
        return redirect('/app')

    token = request.args.get("token")
    if token is not None:
        user = users_utils.verify_jwt_token(token)

        if user is None:
            redirect('/')

        form = forms.ResetPasswordForm()

        if form.validate_on_submit():
            user.set_password(form.new_password.data)
            session.commit()

            redirect('/login')

        return redirect('auth/reset_password.html')
    else:
        form = forms.ResetPasswordRequestForm()

        if form.validate_on_submit():
            user = users_utils.get_user(email=form.email.data)
            if user is not None:
                email.send_reset_password_email(user)

            flash("Проверьте свою почту для интрукций по сбросу пароля")
            return redirect('/login')

        return render_template("auth/reset_password_request.html", form=form)
