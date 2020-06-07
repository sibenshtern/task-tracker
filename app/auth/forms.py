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


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Reset password")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField(
        validators=[
            DataRequired(),
            EqualTo('confirm_new_password', message="Пароли должны совпадать")
        ]
    )
    confirm_new_password = PasswordField(
        validators=[
            DataRequired(),
            EqualTo('new_password', message="Пароли должны совпадать")
        ]
    )
    submit = SubmitField("Изменить пароль")


class MailRequestForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Verify user")
