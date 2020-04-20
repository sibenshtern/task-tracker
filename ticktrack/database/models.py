import datetime

from pymodm import MongoModel, EmbeddedMongoModel, fields
from pymongo.write_concern import WriteConcern

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Mark(EmbeddedMongoModel):
    id = fields.IntegerField(primary_key=True)
    title = fields.CharField(min_length=1, required=True)
    color = fields.CharField(min_length=6)

    class Meta:
        final = True


class TaskLine(EmbeddedMongoModel):
    done = fields.BooleanField(default=False)
    body = fields.CharField()

    def finish(self):
        self.done = True


class Task(EmbeddedMongoModel):
    id = fields.IntegerField(primary_key=True)
    title = fields.CharField(default="Untitled")

    marks = fields.EmbeddedDocumentListField(Mark)
    lines = fields.EmbeddedDocumentListField(TaskLine)
    modified_date = fields.DateTimeField(default=datetime.datetime.now)
    finish_date = fields.DateTimeField()

    def set_modified_date(self):
        self.modified_date = datetime.datetime.now()

    def set_finish_date(self, date):
        self.finish_date = date


class User(MongoModel, UserMixin):
    id = fields.IntegerField(primary_key=True)
    email = fields.EmailField(required=True)
    hashed_password = fields.CharField(min_length=1)
    name = fields.CharField(required=True, min_length=1)

    tasks = fields.EmbeddedDocumentListField(Task)
    marks = fields.EmbeddedDocumentListField(Mark)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = "mongodb_app"
