import datetime
from string import ascii_letters
from random import choice

from pymodm import MongoModel, EmbeddedMongoModel, fields
from pymongo.write_concern import WriteConcern

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Mark(EmbeddedMongoModel):
    id = fields.IntegerField(primary_key=True)
    title = fields.CharField(min_length=1, required=True)
    color = fields.CharField(min_length=6)

    def json(self):
        return {'id': self.id, 'title': self.title}

    class Meta:
        final = True


class Task(EmbeddedMongoModel):
    id = fields.IntegerField(primary_key=True)
    title = fields.CharField(default="Untitled")
    finished = fields.BooleanField(default=False)

    marks = fields.EmbeddedDocumentListField(Mark)
    modified_date = fields.DateTimeField(default=datetime.datetime.now)
    finish_date = fields.DateTimeField()

    def set_modified_date(self):
        self.modified_date = datetime.datetime.now()

    def set_finish_date(self, date):
        self.finish_date = date

    def change_status(self):
        self.finished = not self.finished

    def json(self):
        return {
            'id': self.id, 'title': self.title, 'finished': self.finished,
            'marks': [mark.json() for mark in self.marks],
            'finish_date': str(self.finish_date)
        }


class User(MongoModel, UserMixin):
    id = fields.IntegerField(primary_key=True)
    email = fields.EmailField(required=True)
    hashed_password = fields.CharField(min_length=1)
    apikey = fields.CharField()
    name = fields.CharField(required=True, min_length=1)

    tasks = fields.EmbeddedDocumentListField(Task)
    marks = fields.EmbeddedDocumentListField(Mark)

    def generate_apikey(self):
        symbols = list(ascii_letters) + list('1234567890')
        self.apikey = ''.join(choice(symbols) for _ in range(30))
        print(self.apikey)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def return_apikey(self):
        return self.apikey

    class Meta:
        cascade = True
        write_concern = WriteConcern(j=True)
        connection_alias = "mongodb_app"
