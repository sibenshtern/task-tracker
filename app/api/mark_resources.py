from flask import jsonify

from flask_restful import Resource
from flask_restful import reqparse

from . import utils as api_utils
from app.database.utils import labels_utils


parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, location='args')

LABEL_ARGS = ("id", "user_id", "title", "color")
LABEL_TYPE = "label"


class LabelResource(Resource):

    def get(self, apikey, label_id):
        user = api_utils.check_and_return_user_by_apikey(apikey)
        self.check_label_id(user, label_id)
        return {
                'error': False,
                'status_code': 200,
                'object': {
                    "type": LABEL_TYPE,
                    "content": labels_utils.get_label(
                        user.id, label_id=label_id
                    ).to_dict(only=LABEL_ARGS)
                }
            }, 200

    def put(self, apikey, label_id):
        args = parser.parse_args()
        user = api_utils.check_and_return_user_by_apikey(apikey)
        self.check_label_id(user, label_id)

        # Проверяю, что название задачи правильное
        if not 1 < len(args.title) < 16:
            return {
                'error': True,
                'status_code': 404,
                'error_message':
                    "Label's length must be more than 1, but less than 16"
            }, 404

        label = labels_utils.get_label(user.id, label_id=label_id)
        label.title = args.title
        labels_utils.session.commit()

        return {
                'error': False,
                'status_code': 200,
                'object': {
                    'type': LABEL_TYPE,
                    'content': label.to_dict(only=LABEL_ARGS),
                    'status': 'updated'
                }
            }, 200

    def delete(self, apikey, label_id):
        user = api_utils.check_and_return_user_by_apikey(apikey)
        self.check_label_id(user, label_id)

        label = labels_utils.get_label(user.id, label_id=label_id)
        labels_utils.delete_label(user.id, label_id=label_id)

        return {
                'error': False,
                'status_code': 200,
                'object': {
                    'type': LABEL_TYPE,
                    'content': label.to_dict(only=LABEL_ARGS),
                    'status': 'deleted'
                }
            }, 200

    @staticmethod
    def check_label_id(user, label_id):
        label_obj = {
            'obj': 'mark', 'user_id': user.id, 'label_id': label_id,
            'message': 'Invalid mark ID'
        }
        api_utils.abort_if_obj_doesnt_exist(label_obj)


class LabelListResource(Resource):

    @staticmethod
    def get(apikey):
        user = api_utils.check_and_return_user_by_apikey(apikey)

        return {
                'error': False,
                'status_code': 200,
                'objects': [
                    label.to_dict(only=LABEL_ARGS)
                    for label in labels_utils.get_labels(user.id)
                ]
            }, 200

    @staticmethod
    def post(apikey):
        args = parser.parse_args()
        user = api_utils.check_and_return_user_by_apikey(apikey)

        if not 1 < len(args.title) < 16:
            return {
                'error': True,
                'status_code': 404,
                'error_message':
                    "Label's length must be more than 1, but less than 16"
            }, 404

        labels_utils.create_label(user.id, args.title)
        return {
                'error': False,
                'status_code': 200,
                'object':
                    labels_utils.get_label(
                        user.id, title=args.title
                    ).to_dict(only=LABEL_ARGS),
                'status': 'created'
            }, 200
