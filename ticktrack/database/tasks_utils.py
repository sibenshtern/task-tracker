import datetime

from pymodm.errors import DoesNotExist
from flask_login import current_user

from ticktrack.database.models import Task
from ticktrack.database import users_utils


def search_max_id_in_tasks():
    try:
        all_tasks = current_user.tasks
        return max(all_tasks, key=lambda mark: mark.id).id
    except DoesNotExist:
        return 0
    except ValueError:
        return 0


def create_task(title, marks, finish_date):
    task = Task(id=search_max_id_in_tasks() + 1, title=title)

    if len(marks) > 0:
        task.marks = marks

    task.set_finish_date(finish_date)

    current_user.tasks.append(task)
    current_user.save()


def return_today_tasks(user_id: int):
    user = users_utils.return_user(user_id)

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
    user = users_utils.return_user(user_id)

    if user is not None:
        return user.tasks
    return None


def return_task(user_id, task_id):
    user = users_utils.return_user(user_id)

    if user is not None:
        for task in user.tasks:
            if task.id == task_id:
                return task
    return None
