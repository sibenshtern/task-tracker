from flask import Blueprint
from flask import render_template

from flask_login import login_user, login_required, logout_user

from werkzeug.utils import redirect

from ticktrack.auth import forms
import ticktrack.database as database


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/logout')
def logout():
    logout_user()
    return 'logout'


@blueprint.route('/login', methods=['GET', 'POST'])
def login_page():
    form = forms.LoginForm()

    if form.validate_on_submit():
        user = database.return_user(email=form.email.data.strip())
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/app/all')
        return 'Неправильно что-то'

    return render_template('auth/login.html', form=form)


@blueprint.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = forms.SignupForm()

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'auth/signup.html', form=form, title='Регистрация'
            )
        if database.return_user(email=form.email.data):
            return 'Нашел такого пользователя'

        database.create_user(
            form.email.data, form.password.data, form.name.data
        )

        return redirect('/login')

    return render_template('auth/signup.html', form=form)
