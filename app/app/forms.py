import datetime

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import DateField


class AddMarkForm(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(min=1, max=16)])
    submit = SubmitField('Добавить метку')


class AddTaskForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    marks = SelectMultipleField()
    finish_date = DateField(default=datetime.date.today(), validators=[DataRequired()])
    submit = SubmitField('Добавить задачу')


class EditMarkForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    edit_button = SubmitField('Изменить метку')
    delete_button = SubmitField('Удалить метку')


class EditTaskForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    marks = SelectMultipleField()
    finish_date = DateField(validators=[DataRequired()])
    edit_submit = SubmitField('Изменить задачу')
    delete_submit = SubmitField('Удалить задачу')
