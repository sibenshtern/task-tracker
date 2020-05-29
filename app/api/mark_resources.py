from flask import jsonify

from flask_restful import Resource
from flask_restful import reqparse

from marshmallow import ValidationError

from . import utils as api_utils
from app.database.utils import labels_utils, users_utils

from .schema import MarkSchema


parser = reqparse.RequestParser()

parser.add_argument('title', type=str, required=True)

LABELS_ARGS = ("id", "user_id", "title", "color")


class MarkResource(Resource):

    def get(self, apikey, label_id):
        api_utils.check_apikey(apikey)
        # Если apikey неправильный, то функция вызовет abort,
        # что приведет к выходу из функции get

        user = users_utils.get_user(apikey=apikey)
        self.check_label_id(user, label_id)

        return jsonify({
            'label':
                labels_utils.get_label(user.id, label_id=label_id).to_dict(
                    only=LABELS_ARGS
                )
        })

    def put(self, apikey, label_id):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.get_user(apikey=apikey)

        self.check_label_id(user, label_id)

        try:
            result = MarkSchema().load({'title': args.title})
        except ValidationError as error:
            return jsonify(
                {'status': 'Something went wrong', 'errors': error.messages}
            )
        for label in labels_utils.get_labels(user.id):
            if label.id == label_id:
                label.title = result['title']
                labels_utils.session.commit()

        return jsonify(
            {'status': 'OK', 'message': f'Update mark with ID: {label_id}'}
        )

    def delete(self, apikey, label_id):
        api_utils.check_apikey(apikey)
        user = users_utils.get_user(apikey=apikey)
        self.check_label_id(user, label_id)

        labels_utils.delete_label(user.id, label_id=label_id)

        return jsonify(
            {
                'status': 'OK',
                'message': f'Successful delete mark with ID: {label_id}'
            }
        )

    @staticmethod
    def check_label_id(user, label_id):
        label_obj = {
            'obj': 'mark', 'user_id': user.id, 'label_id': label_id,
            'message': 'Invalid mark ID'
        }
        api_utils.abort_if_obj_doesnt_exist(label_obj)


class MarkListResource(Resource):

    def get(self, apikey):
        api_utils.check_apikey(apikey)
        user = users_utils.get_user(apikey=apikey)

        return jsonify({
            'marks': [
                mark.to_dict(only=LABELS_ARGS)
                for mark in labels_utils.get_labels(user.id)
            ]
        })

    def post(self, apikey):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.get_user(apikey=apikey)

        try:
            MarkSchema().load({'title': args.title})
        except ValidationError as error:
            return jsonify(
                {'status': 'Something went wrong', 'errors': error.messages}
            )

        labels_utils.create_label(user, args.title)
        return jsonify(
            {
                'status': 'OK',
                'message': f"Successful create mark with title: {args.title}"
            }
        )
