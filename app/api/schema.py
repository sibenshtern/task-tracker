from datetime import date

from marshmallow import ValidationError, Schema, validates
from marshmallow.fields import Str, Date
from marshmallow.validate import Length


FINISH_DATE_FORMAT = "%d.%m.%Y"


class TaskSchema(Schema):
    title = Str(validate=Length(min=1, max=256), required=True)
    labels = Str()
    finish_date = Date(format=FINISH_DATE_FORMAT)

    @validates('labels')
    def marks_validator(self, labels):
        labels_list = labels.split(';')

        for label_id in labels_list:
            if not label_id.isdigit():
                raise ValidationError('Label ID must be integer')

    @validates('finish_date')
    def validate_finish_date(self, value: date):
        if value < date.today():
            raise ValidationError("Finish date can't be in past")
