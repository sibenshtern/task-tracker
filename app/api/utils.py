from flask_restful import abort
from app.database.utils import users_utils, tasks_utils, labels_utils


def abort_if_obj_doesnt_exist(obj):
    if obj['obj'].startswith('user') and users_utils.get_user(
            apikey=obj['apikey']) is None:
        abort(404, message=obj['message'])
    elif obj['obj'].startswith('task') and tasks_utils.get_task(
            obj['user_id'], task_id=obj['task_id']) is None:
        abort(404, message=obj['message'])
    elif obj['obj'].startswith('label') and labels_utils.get_label(
            obj['user_id'], label_id=obj['label_id']) is None:
        abort(404, message=obj['message'])


def check_apikey(apikey):
    user_obj = {
        'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey'
    }
    abort_if_obj_doesnt_exist(user_obj)
