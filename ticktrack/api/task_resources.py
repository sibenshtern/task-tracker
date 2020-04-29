from datetime import datetime

from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from marshmallow import ValidationError

from . import utils as api_utils
from ticktrack.database import users_utils, tasks_utils, marks_utils

from .sсhema import TaskSchema

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True)
parser.add_argument('mark_ids', type=str, required=True)
parser.add_argument('finish_date', type=str, required=True)

# Аргумент, специально для PUT запроса
parser.add_argument(
    'action', choices=('change_status'), help="Bas choice: {error_msg}."
)


class TaskResource(Resource):

    def get(self, apikey, task_id):

        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_task_id(user, task_id)

        task = tasks_utils.return_task(user.id, task_id)
        return task.json()

    def put(self, apikey, task_id):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_task_id(user, task_id)

        if args.action:
            if args.action.startswith('change_status'):
                for task in user.tasks:
                    if task.id == task_id:
                        task.finished = not task.finished
                user.save()
                return jsonify({'status': 'OK', 'message': 'status changed'})
        else:
            return abort(404, message="Action is required")

    @staticmethod
    def check_task_id(user, task_id):
        task_obj = {
            'obj': 'task', 'user_id': user.id, 'task_id': task_id,
            'message': f"Task with ID: {task_id} not found"
        }
        return api_utils.abort_if_object_doesnt_exist(task_obj) is None


class TaskListResource(Resource):

    def get(self, apikey):
        self.check_apikey(apikey)

        user = users_utils.return_user(apikey=apikey)
        return jsonify([task.json() for task in user.tasks])

    def post(self, apikey):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        try:
            finish_date = datetime.strptime(args.finish_date, "%d.%m.%Y")
        except ValueError:
            abort(404, message='Invalid finish date format')

        task_scheme = TaskSchema()

        try:
            print(args.title)
            result = task_scheme.load(
                {
                    'title': args.title,
                    'marks': args.mark_ids,
                    'finish_date': finish_date.strftime('%d.%m.%Y')  # noqa
                }
            )
        except ValidationError as error:
            abort(404, message=error.messages)

        marks_ids = list(map(int, result['marks'].split(';')))  # noqa

        marks_objects = [
            marks_utils.return_mark(user.id, mark_id)
            for mark_id in marks_ids
            if marks_utils.return_mark(user.id, mark_id) is not None
        ]

        tasks_utils.create_task(
            user, result['title'], marks_objects, finish_date
        )
        return jsonify({'result': 'Create Task'})

    @staticmethod
    def check_apikey(apikey: str):
        user_obj = {
            'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey.'
        }
        return api_utils.abort_if_object_doesnt_exist(user_obj) is None
