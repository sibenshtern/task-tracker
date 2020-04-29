from flask_login import current_user
from pymodm.errors import DoesNotExist

from ticktrack.database.models import Mark
from ticktrack.database import users_utils


def search_max_id_in_marks(user):
    try:
        all_marks = user.marks
        return max(all_marks, key=lambda mark: mark.id).id
    except DoesNotExist:
        return 0
    except ValueError:
        return 0


def create_mark(user, title):
    mark = Mark(id=search_max_id_in_marks(user) + 1, title=title)
    user.marks.append(mark)
    user.save()


def return_mark(user_id, mark_id: int = None, title: str = None):
    if mark_id is not None:
        for mark in users_utils.return_user(user_id).marks:
            if mark.id == mark_id:
                return mark
    elif title is not None:
        for mark in users_utils.return_user(user_id).marks:
            if mark.title == title:
                return mark
    return None


def return_marks(user_id: int):
    user = users_utils.return_user(user_id)

    if user is not None:
        return user.marks
    return None
