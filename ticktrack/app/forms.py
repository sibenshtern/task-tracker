import datetime

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length


class AddMarkForm(FlaskForm):
    title = StringField(validators=[DataRequired(), Length(min=1, max=16)])
    submit = SubmitField('Добавить метку')


class AddTaskForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    marks = SelectMultipleField()
    finish_date = DateField(default=datetime.date.today(), validators=[DataRequired()])
    submit = SubmitField('Добавить задачу')


class EditMark(FlaskForm):
    title = StringField(validators=[DataRequired()])

