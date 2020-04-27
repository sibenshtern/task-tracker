from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from ticktrack.api import utils as api_utils
from ticktrack.database import users_utils, tasks_utils, marks_utils
from ticktrack.database.models import User, Task

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)
parser.add_argument('marks', type=list)
parser.add_argument('finish_date', type=str)

# Аргумент, специально для PUT запроса
parser.add_argument(
    'action', choices=('change_status', 'update'), type=str,
    help="Bas choice: {error_msg}. Possible values: change_status, update"
)


class TaskResource(Resource):

    def get(self, apikey, task_id):

        self.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_task_id(user, task_id)

        task = tasks_utils.return_task(user.id, task_id)
        return task.json()

    # def post(self, apikey, task_id):
    #     args = parser.parse_args()
    #
    #     self.check_apikey(apikey)

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

        if args.title:
            pass



    @staticmethod
    def check_apikey(apikey):
        user_obj = {
            'obj': 'user', 'apikey': apikey, 'message': 'Invalid apikey'
        }
        return api_utils.abort_if_object_doesnt_exist(user_obj) is None

