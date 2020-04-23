import datetime

from flask import current_app
from pymodm.errors import DoesNotExist

from ticktrack.database.models import User, Task


def search_max_id():
    try:
        all_users = User.objects.all().values()
        return max(all_users, key=lambda user: user["_id"])["_id"]
    except DoesNotExist:
        return 1
    except ValueError:
        return 1


def create_user(email: str = None, name: str = None, password: str = None):
    users = User(id=current_app.max_id, email=email, name=name)
    users.set_password(password)
    users.save()

    current_app.max_id += 1


def return_user(user_id: int = None, email: str = None):
    try:
        if user_id is not None:
            return User.objects.get({'_id': user_id})
        elif email is not None:
            return User.objects.get({'email': email})
        else:
            raise ValueError("You don't give any arguments")
    except DoesNotExist:
        return None


def return_today_tasks(user_id: int):
    user = return_user(user_id)

    if user is not None:
        user_tasks = user.tasks
        today_tasks = []
        for task in user_tasks:
            now_date = datetime.date.today()

            now_datetime = datetime.datetime(now_date.year, now_date.month,
                                             now_date.day)
            if task.finish_date == now_datetime:
                today_tasks.append(task)

        return today_tasks
    return None


def return_all_tasks(user_id):
    user = return_user(user_id)

    if user is not None:
        return user.tasks
    return None


def return_marks(user_id: int):
    user = return_user(user_id)

    if user is not None:
        user_marks = [mark.json() for mark in user.marks]
        return user_marks
    return None
