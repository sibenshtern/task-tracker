from flask import jsonify

from flask_restful import Resource
from flask_restful import abort, reqparse

from marshmallow import ValidationError

from . import utils as api_utils
from ticktrack.database import marks_utils, users_utils

from .sсhema import MarkSchema


parser = reqparse.RequestParser()

parser.add_argument('title', type=str, required=True)


class MarkResource(Resource):

    def get(self, apikey, mark_id):
        api_utils.check_apikey(apikey)
        # Если apikey неправильный, то функция вызовет abort,
        # что приведет к выходу из функции get

        user = users_utils.return_user(apikey=apikey)


    def delete(self, apikey, mark_id):
        api_utils.check_apikey(apikey)


    @staticmethod
    def check_mark_id(user, mark_id):
        mark_obj = {
            'user_id': user.id, 'mark_id': mark_id,
            'message': 'Invalid mark ID'
        }
        api_utils.abort_if_object_doesnt_exist(mark_obj)

