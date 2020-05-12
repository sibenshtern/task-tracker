from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from marshmallow import ValidationError

from ticktrack.api import utils as api_utils
from ticktrack.database import marks_utils, users_utils

from ticktrack.api.schema import MarkSchema


parser = reqparse.RequestParser()

parser.add_argument('title', type=str, required=True)


class MarkResource(Resource):

    def get(self, apikey, mark_id):
        api_utils.check_apikey(apikey)
        # Если apikey неправильный, то функция вызовет abort,
        # что приведет к выходу из функции get

        user = users_utils.return_user(apikey=apikey)
        self.check_mark_id(user, mark_id)

        return jsonify(
            {'mark': marks_utils.return_mark(user.id, mark_id).json()}
        )

    def put(self, apikey, mark_id):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        self.check_mark_id(user, mark_id)

        try:
            result = MarkSchema().load({'title': args.title})
        except ValidationError as error:
            return jsonify(
                {'status': 'Something went wrong', 'errors': error.messages}
            )
        for mark in user.marks:
            if mark.id == mark_id:
                mark.title = result['title']
                user.save()

        return jsonify(
            {'status': 'OK', 'message': f'Update mark with ID: {mark_id}'}
        )

    def delete(self, apikey, mark_id):
        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)
        self.check_mark_id(user, mark_id)

        for index in range(len(user.marks)):
            if user.marks[index].id == mark_id:
                if len(user.marks) > 1:
                    del user.marks[index]
                else:
                    del user.marks
                user.save()
                break

        return jsonify(
            {
                'status': 'OK',
                'message': f'Successful delete mark with ID: {mark_id}'
            }
        )

    @staticmethod
    def check_mark_id(user, mark_id):
        mark_obj = {
            'obj': 'mark', 'user_id': user.id, 'mark_id': mark_id,
            'message': 'Invalid mark ID'
        }
        api_utils.abort_if_object_doesnt_exist(mark_obj)


class MarkListResource(Resource):

    def get(self, apikey):
        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        return jsonify({'marks': [mark.json() for mark in user.marks]})

    def post(self, apikey):
        args = parser.parse_args()

        api_utils.check_apikey(apikey)
        user = users_utils.return_user(apikey=apikey)

        try:
            MarkSchema().load({'title': args.title})
        except ValidationError as error:
            return jsonify(
                {'status': 'Something went wrong', 'errors': error.messages}
            )

        marks_utils.create_mark(user, args.title)
        return jsonify(
            {
                'status': 'OK',
                'message': f"Successful create mark with title: {args.title}"
            }
        )
