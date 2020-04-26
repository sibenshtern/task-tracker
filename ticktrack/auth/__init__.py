from flask import Blueprint
from flask import render_template

from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.utils import redirect

from ticktrack.auth import forms
from ticktrack.database import users_utils


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
        user = users_utils.return_user(email=form.email.data.strip())
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect('/app/all')

        return render_template(
            'auth/login.html', form=form,
            message="Неправильный логин или пароль. Повторите попытку",
            current_user=current_user
        )

    return render_template(
        'auth/login.html', form=form, message=None, current_user=current_user
    )


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
        if users_utils.return_user(email=form.email.data) is not None:
            return render_template(
                'auth/signup.html', form=form, title='Регистрация',
                message="Пользователь с такой почтой уже зарегистрирован. "
                        "Повторите попытку",
                current_user=current_user
            )

        users_utils.create_user(
            form.email.data, form.name.data, form.password.data
        )

        return redirect('/login')

    return render_template(
        'auth/signup.html', form=form, message=None, current_user=current_user
    )
