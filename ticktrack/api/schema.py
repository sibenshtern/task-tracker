from datetime import date

from marshmallow import ValidationError, Schema, validates
from marshmallow.fields import Str, Date
from marshmallow.validate import Length

from ticktrack.database.marks_utils import return_mark


FINISH_DATE_FORMAT = "%d.%m.%Y"


class TaskSchema(Schema):
    title = Str(validate=Length(min=1, max=256), required=True)
    marks = Str()
    finish_date = Date(format=FINISH_DATE_FORMAT, required=True)

    @validates('marks')
    def marks_validator(self, marks):
        marks_list = marks.split(';')

        for mark_id in marks_list:
            if not mark_id.isdigit():
                raise ValidationError('Mark ID must be integer')

    @validates('finish_date')
    def validate_finish_date(self, value: date):
        if value < date.today():
            raise ValidationError("Finish date can't be in past")


class MarkSchema(Schema):
    title = Str(validate=Length(min=1, max=16), required=True)
