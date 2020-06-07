from flask_restful import abort
from app.database.utils import users_utils, tasks_utils, labels_utils


USER = "user"
TASK = "task"
LABEL = "label"


def abort_if_obj_doesnt_exist(obj):
    if obj['obj'].startswith(USER) and users_utils.get_user(
                apikey=obj['apikey']
            ) is None:
        abort(404, message=obj['message'])
    elif obj['obj'].startswith(TASK) and tasks_utils.get_task(
                obj['user_id'], task_id=obj['task_id']
            ) is None:
        abort(404, message=obj['message'])
    elif obj['obj'].startswith(LABEL) and labels_utils.get_label(
                    obj['user_id'], label_id=obj['label_id']
            ) is None:
        abort(404, message=obj['message'])


def check_and_return_user_by_apikey(apikey):
    user_obj = {
        "obj": USER,
        "apikey": apikey,
        "message": "Nonexistent API key"
    }

    abort_if_obj_doesnt_exist(user_obj)
    user = users_utils.get_user(apikey=apikey)

    if not user.is_verified:
        abort(404, message="User isn't verified")

    return user


