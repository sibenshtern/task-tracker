import datetime
from random import shuffle

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy
from sqlalchemy import Integer, String, Boolean, Date, orm
from sqlalchemy_serializer import SerializerMixin

from . import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin, UserMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(String)

    email = sqlalchemy.Column(String)
    hashed_password = sqlalchemy.Column(String, nullable=True)
    apikey = sqlalchemy.Column(String, unique=True, nullable=True)

    is_verified = sqlalchemy.Column(Boolean, default=False)

    def generate_apikey(self):
        if self.apikey is None:
            possible_symbols = list(''.join([self.name, self.email]))
            shuffle(possible_symbols)
            pre_apikey = ''.join(possible_symbols)
            self.apikey = generate_password_hash(pre_apikey).split('$')[-1]
        else:
            raise Exception("API key already generated")

    def set_password(self, password: str) -> None:
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    def verify(self):
        self.is_verified = True


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tasks"

    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(Integer, sqlalchemy.ForeignKey("users.id"))

    title = sqlalchemy.Column(String, default="Untitled", nullable=True)
    is_finished = sqlalchemy.Column(Boolean, default=False)
    
    labels = orm.relationship(
        'Label', secondary="tasks_to_labels", backref="tasks"
    )

    modified_date = sqlalchemy.Column(Date, default=datetime.date.today())
    finish_date = sqlalchemy.Column(Date, nullable=True)

    def change_modified_date(self):
        self.modified_date = datetime.date.today()

    def change_finish_date(self, date: datetime.date):
        self.finish_date = date

    def change_status(self):
        self.is_finished = not self.is_finished


class Label(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "labels"

    serialize_only = ("id", "user_id", "title", "color")

    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(Integer, sqlalchemy.ForeignKey('users.id'))

    title = sqlalchemy.Column(String)
    color = sqlalchemy.Column(String, nullable=True)


association_table = sqlalchemy.Table(
    'tasks_to_labels', SqlAlchemyBase.metadata,
    sqlalchemy.Column('tasks', Integer, sqlalchemy.ForeignKey('tasks.id')),
    sqlalchemy.Column('labels', Integer, sqlalchemy.ForeignKey('labels.id'))
)


