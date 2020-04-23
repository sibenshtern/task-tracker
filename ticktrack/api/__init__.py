from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from ticktrack.database import utils as db_utils
from ticktrack.database.models import User, Task

parser = reqparse.RequestParser()
parser.add_argument('apikey', required=True)
parser.add_argument('task_id', type=int)
parser.add_argument('mark_id', type=int)


class TaskResource(Resource):

    @staticmethod
    def get():
        args = parser.parse_args()

        apikey = args['apikey']
        task_id = args['task_id']

        if db_utils.return_user(apikey=apikey) is None:
            abort(404, message="Wrong apikey")
        else:
            user = db_utils.return_user(apikey=apikey)

            abort_if_task_not_found(user.id, task_id)
            task = db_utils.return_task(user.id, task_id)
            return jsonify({
                'status': 'success',
                'response': {
                    'id': task.id,
                    'title': task.title,
                    'finished': task.finished,
                    'marks': task.marks,
                    'finish_date': task.finish_date
                }
            })

    @staticmethod
    def post(task_id):
        pass

    @staticmethod
    def put():
        args = parser.parse_args()

        apikey = args['apikey']
        task_id = args['task_id']

        if db_utils.return_user(apikey=apikey) is None:
            abort(404, message="Wrong apikey")
        else:
            user = db_utils.return_user(apikey=apikey)
            task = user.tasks[task_id - 1]
            task.finished = not task.finished
            user.save()
            return jsonify({'success': True})

    @staticmethod
    def delete():
        args = parser.parse_args()
        apikey = args['apikey']
        mark_id = args['mark_id']

        if db_utils.return_user(apikey=apikey) is None:
            abort(404, message="Wrong apikey")
        else:
            user = db_utils.return_user(apikey=apikey)
            for index in range(len(user.marks)):
                if user.marks[index].id == mark_id:
                    if len(user.marks) > 1:
                        del user.marks[index]
                    else:
                        del user.marks
            user.save()
            return jsonify({'success': True})


def abort_if_task_not_found(user_id, task_id):
    task = db_utils.return_task(user_id, task_id)

    if task is not None:
        return None
    abort(404)


def abort_if_mark_not_found(apikey, mark_id):
    pass


def get_user_id_by_apikey(apikey):
    user = db_utils.return_user(apikey=apikey)

    if user is not None:
        return user.id
    return None

