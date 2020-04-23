from flask import Blueprint
from flask import render_template

from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.utils import redirect

from ticktrack.auth import forms
import ticktrack.database as database


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
        user = database.return_user(email=form.email.data.strip())
        if user and user.check_password(form.password.data):
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
        if database.return_user(email=form.email.data):
            return render_template(
                'auth/signup.html', form=form, title='Регистрация',
                message="Пользователь с такой почтой уже зарегистрирован. "
                        "Повторите попытку"
            )

        database.create_user(
            form.email.data, form.password.data, form.name.data
        )

        return redirect('/login')

    return render_template('auth/signup.html', form=form, message=None)
