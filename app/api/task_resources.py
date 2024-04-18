from datetime import datetime

from flask import jsonify

from flask_restful import Resource
from flask_restful import reqparse

from marshmallow import ValidationError

from . import utils as api_utils
from app.database.utils import tasks_utils, labels_utils

from .schema import TaskSchema

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, location='args')
parser.add_argument('labels_ids', type=str, location='args')
parser.add_argument('finish_date', type=str, location='args')

# Аргумент, специально для PUT запроса
parser.add_argument(
    'action', choices=('change_status',), help="Bas choice: {error_msg}.",
    location='args'
)
TASK_ARGS = (
    "id", "user_id", "title", "is_finished", "labels", "modified_date",
    "finish_date"
)
TASK_TYPE = 'task'


class TaskResource(Resource):

    def get(self, apikey, task_id):
        user = api_utils.check_and_return_user_by_apikey(apikey)

        self.check_task_id(user, task_id)

        task = tasks_utils.get_task(user.id, task_id)
        return {
                'error': False,
                'status_code': 200,
                'object': {
                    'type': TASK_TYPE,
                    'content': task.to_dict(only=TASK_ARGS)
                }
            }

    def put(self, apikey, task_id):
        args = parser.parse_args()

        user = api_utils.check_and_return_user_by_apikey(apikey)
        self.check_task_id(user, task_id)

        if args['action']:
            if args['action'].startswith('change_status'):
                task = tasks_utils.get_task(user.id, task_id)
                task.change_status()
                tasks_utils.session.commit()
                return {
                        'error': False,
                        'status_code': 200,
                        'object': task.to_dict(only=TASK_ARGS),
                        'status': 'updated'
                    }
        else:
            return {
                'error': True,
                'status_code': 404,
                'error_messages': ['Action is required']
            }

    def delete(self, apikey, task_id):
        user = api_utils.check_and_return_user_by_apikey(apikey)
        self.check_task_id(user, task_id)

        task = tasks_utils.get_task(user.id, task_id)
        tasks_utils.delete_task(user.id, task_id)

        return {
                'error': False,
                'status_code': 200,
                'object': {
                    'type': TASK_TYPE,
                    'content': task.to_dict(only=TASK_ARGS)
                },
                'status': 'deleted'
            }

    @staticmethod
    def check_task_id(user, task_id):
        task_obj = {
            'obj': 'task', 'user_id': user.id, 'task_id': task_id,
            'message': f"Task with ID: {task_id} not found"
        }
        return api_utils.abort_if_obj_doesnt_exist(task_obj) is None


class TaskListResource(Resource):

    def get(self, apikey):
        user = api_utils.check_and_return_user_by_apikey(apikey)

        return jsonify(
            {
                'error': False,
                'objects': [
                    task.to_dict(only=TASK_ARGS)
                    for task in tasks_utils.get_tasks(user.id)
                ]
            }
        )

    def post(self, apikey):
        args = parser.parse_args()
        user = api_utils.check_and_return_user_by_apikey(apikey)

        labels_ids_argument = False
        finish_date_argument = False

        if args.get("title") is None:
            return {
                'error': True,
                'status_code': 404,
                'error_messages': ['Title is required']
            }, 404
        if args.get('labels_ids') is not None:
            labels_ids_argument = True
        if args.get('finish_date') is not None:
            finish_date_argument = True

        if finish_date_argument:
            try:
                finish_date = datetime.strptime(args.finish_date, "%d.%m.%Y")
            except ValueError:
                return {
                    'error': True,
                    'status_code': 404,
                    'error_messages': ['Invalid date format']
                }

        task_scheme = TaskSchema()

        # Проверяю, что переданные в запросе параметры правильные
        payloads = {'title': args.title}  # словарь для проверки

        # Проверяю, что пользователь передал аргументы, чтобы не
        # вызвать ошибку

        if labels_ids_argument:
            payloads['labels'] = args.labels_ids
        if finish_date_argument:
            payloads['finish_date'] = finish_date.strftime('%d.%m.%Y')  # noqa

        try:
            result = task_scheme.load(payloads)
        except ValidationError as error:
            return {
                'error': True,
                'status_code': 404,
                'error_messages': error.messages
            }, 404

        if labels_ids_argument:
            labels_ids = list(map(int, result['labels'].split(';')))  # noqa

            labels_objects = [
                labels_utils.get_label(user.id, label_id=label_id)
                for label_id in labels_ids
                if labels_utils.get_label(
                    user.id, label_id=label_id
                ) is not None
            ]

        task_arguments = {
            'title': result['title'],
            'labels': []
        }

        if labels_ids_argument:
            task_arguments['labels'] = labels_objects  # noqa
        if finish_date_argument:
            task_arguments['finish_date'] = finish_date

        task = tasks_utils.create_task(user.id, **task_arguments)
        return jsonify(
            {
                'error': False,
                'status_code': 200,
                'object': task.to_dict(only=TASK_ARGS),
                'status': 'created'
            }
        )
