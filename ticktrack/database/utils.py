import datetime

from flask import current_app
from flask_login import current_user
from pymodm.errors import DoesNotExist

from ticktrack.database.models import User, Task, Mark


def search_max_id_in_users():
    try:
        all_users = User.objects.all().values()
        return max(all_users, key=lambda user: user["_id"])["_id"]
    except DoesNotExist:
        return 1
    except ValueError:
        return 1


def search_max_id_in_marks():
    try:
        all_marks = current_user.marks
        return max(all_marks, key=lambda mark: mark.id).id
    except DoesNotExist:
        return 0
    except ValueError:
        return 0


def search_max_id_in_tasks():
    try:
        all_tasks = current_user.tasks
        return max(all_tasks, key=lambda mark: mark.id).id
    except DoesNotExist:
        return 0
    except ValueError:
        return 0


def create_user(email: str = None, name: str = None, password: str = None):
    users = User(id=current_app.max_id, email=email, name=name)
    users.generate_apikey()
    users.set_password(password)
    users.save()

    current_app.max_id += 1


def create_mark(title):
    mark = Mark(id=search_max_id_in_marks() + 1, title=title)
    current_user.marks.append(mark)
    current_user.save()


def create_task(title):
    mark = Task(id=search_max_id_in_tasks() + 1, title=title)
    current_user.tasks.append(mark)
    current_user.save()


def return_user(user_id: int = None, email: str = None, apikey: str = None):
    try:
        if user_id is not None:
            return User.objects.get({'_id': user_id})
        elif email is not None:
            return User.objects.get({'email': email})
        elif apikey is not None:
            return User.objects.get({'apikey': apikey})
        else:
            raise ValueError("You don't give any arguments")
    except DoesNotExist:
        return None


def return_mark(mark_id: int = None, title: str = None):
    if mark_id is not None:
        if mark_id < len(current_user.marks):
            return current_user.marks[mark_id]
        else:
            return None
    elif title is not None:
        for mark in current_user.marks:
            if mark.title == title:
                return mark
        else:
            return None
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


def return_task(user_id, task_id):
    user = return_user(user_id)

    if user is not None:
        task = user.tasks[task_id - 1]
        return task

    return None


def return_marks(user_id: int):
    user = return_user(user_id)

    if user is not None:
        return user.marks
    return None
