from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from ticktrack.api import utils as api_utils
from ticktrack.database import utils as db_utils
from ticktrack.database.models import User, Task

parser = reqparse.RequestParser()

parser.add_argument('apikey', required=True)
parser.add_argument('task_id', type=int)
parser.add_argument('mark_id', type=int)
parser.add_argument('title', type=str)
parser.add_argument(
    'action', choices=('change_status', 'update'), type=str,
    help="Bas choice: {error_msg}. "
         "Possible values: 'change_status' and 'update'")


class OpenTaskResource(Resource):

    def get(self):
        args = parser.parse_args()

        self.check_apikey(args.apikey)
        user = db_utils.return_user(apikey=args.apikey)

        if args.task_id:
            task_obj = {
                'obj': 'task', 'user_id': user.id, 'task_id': args.task_id,
                'message': f"Task with ID: {args.task_id} not found"
            }
            api_utils.abort_if_object_doesnt_exist(task_obj)

            task = db_utils.return_task(user.id, args.task_id)
            return task.json()
        else:
            abort(404, message="Task ID not found")

    def put(self):
        args = parser.parse_args()

        self.check_apikey(args.apikey)
        user = db_utils.return_user(apikey=args.apikey)

        if args.task_id:
            self.check_task_id(user, args.task_id)

            if args.action.startswith('change_status'):
                task = db_utils.return_task(user.id, args.task_id)
                task.change_status()
            elif args.action.startswith('update'):
                task = db_utils.return_task(user.id, args.task_id)

                if args.title:
                    task.title = args.title
            user.save()
        else:
            abort(404, message="Task ID not found")

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






