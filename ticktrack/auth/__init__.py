from flask import Blueprint
from flask import render_template

from ticktrack.auth import forms


blueprint = Blueprint('auth', __name__, template_folder='templates')


@blueprint.route('/login')
def login_page():
    form = forms.LoginForm()
    return render_template('auth/login.html', form=form)


@blueprint.route('/signup')
def signup_page():
    form = forms.SignupForm()
    return render_template('auth/signup.html', form=form)
