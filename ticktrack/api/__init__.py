from datetime import datetime
from typing import List

from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from ticktrack.api import utils as api_utils
from ticktrack.database import users_utils, tasks_utils, marks_utils
from ticktrack.database.models import User, Task

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True)
parser.add_argument('marks', type=str, required=True)
parser.add_argument('finish_date', type=str, required=True)

# Аргумент, специально для PUT запроса
parser.add_argument(
    'action', choices=('change_status', 'update'),
    help="Bas choice: {error_msg}."
)


class TaskResource(Resource):

    def get(self, apikey, task_id):

        self.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_task_id(user, task_id)

        task = tasks_utils.return_task(user.id, task_id)
        return task.json()

    def put(self, apikey, task_id):
        args = parser.parse_args()

        self.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_task_id(user, task_id)

        if args.action:
            if args.action.startswith('change_status'):
                for task in user.tasks:
                    if task.id == task_id:
                        task.finished = not task.finished
                user.save()
                return jsonify({'status': 'OK', 'message': 'status changed'})
            elif args.action.startswith('update'):
                task = tasks_utils.return_task(user.id, task_id)

                if args.title:
                    task.title = args.title
                user.save()
                return jsonify({'status': 'OK', 'message': 'task updated'})
        else:
            return abort(404, message="Action is required")

    @staticmethod
    def check_apikey(apikey):
        user_obj = {
            'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey'
        }
        return api_utils.abort_if_object_doesnt_exist(user_obj) is None

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

        self.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        marks = []
        if self.check_marks(args.marks):
            for mark_id in args.marks.split(';'):
                if mark_id.isdigit():
                    mark = marks_utils.return_mark(user.id, int(mark_id))

                    if mark is not None:
                        marks.append(mark)
        if self.check_date(args.finish_date):
            date_list = tuple(map(int, args.finish_date.split('.')))
            finish_date = datetime(date_list[2], date_list[1], date_list[0])

        if len(args.title) > 1:
            tasks_utils.create_task(
                user, args.title, marks, finish_date  # noqa
            )
            return jsonify({'status': 'OK', 'message': 'create new task'})
        else:
            abort(404, message="Invalid title.")

    @staticmethod
    def check_date(date: str):
        date_list: List[str] = date.split('.')
        if len(date_list) != 3:
            abort(404, message="Invalid date format")
        else:
            if not all(item for item in date_list if item.isdigit()):
                abort(404, message='Invalid date format')

            try:
                finish_date = datetime(
                    int(date_list[2]), int(date_list[1]), int(date_list[0])
                )
            except Exception as error:
                abort(404, message=f"Invalid date format. Error: {error}")

        return True

    @staticmethod
    def check_marks(marks: str):
        marks_list = marks.split(';')
        # Проверяем, правильно ли были переданы id меток
        if len(marks_list) == 1:
            if not marks_list[0].isdigit():
                abort(404, message='Invalid marks format.')
        else:
            return True

    @staticmethod
    def check_apikey(apikey: str):
        user_obj = {
            'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey.'
        }
        return api_utils.abort_if_object_doesnt_exist(user_obj) is None

