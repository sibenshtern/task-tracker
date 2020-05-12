from flask_restful import abort
from ticktrack.database import users_utils, tasks_utils, marks_utils


def abort_if_object_doesnt_exist(obj):
    if obj['obj'].startswith('user'):
        if users_utils.return_user(apikey=obj['apikey']) is None:
            abort(404, message=obj['message'])
        return None
    elif obj['obj'].startswith('task'):
        if tasks_utils.return_task(obj['user_id'], obj['task_id']) is None:
            abort(404, message=obj['message'])
        return None
    elif obj['obj'].startswith('mark') and marks_utils.return_mark(
                obj['user_id'], obj['mark_id']) is None:
            abort(404, message=obj['message'])


def check_apikey(apikey):
    user_obj = {
        'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey'
    }
    abort_if_object_doesnt_exist(user_obj)
