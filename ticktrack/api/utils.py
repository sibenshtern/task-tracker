from flask_restful import abort
from ticktrack.database import tasks_utils


def abort_if_object_doesnt_exist(obj):
    if obj['obj'].startswith('user'):
        if tasks_utils.return_user(apikey=obj['apikey']) is None:
            abort(404, message=obj['message'])
        return None
    elif obj['obj'].startswith('task'):
        if tasks_utils.return_task(obj['user_id'], obj['task_id']) is None:
            abort(404, message=obj['message'])
        return None

