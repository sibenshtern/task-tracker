from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddMarkForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    submit = SubmitField()
