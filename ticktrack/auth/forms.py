from flask_wtf import FlaskForm

from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class SignupForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired()])

    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm = PasswordField(
        'Повторите пароль',
        validators=[
            DataRequired(),
            EqualTo('password', 'Пароли должны совпадать')
        ]
    )
    submit = SubmitField('Зарегистрироваться')
