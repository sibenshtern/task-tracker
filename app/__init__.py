import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from .database import users_utils

from .app import blueprint as app_blueprint
from .auth import blueprint as auth_blueprint
from .about import blueprint as about_blueprint
from .other import blueprint as other_blueprint
from .api.task_resources import TaskResource, TaskListResource
from .api.mark_resources import MarkResource, MarkListResource


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.max_id = users_utils.search_max_id_in_users()

login_manager = LoginManager()
login_manager.init_app(app) # noqa

api = Api(app) # noqa
api.add_resource(TaskResource, '/api/<string:apikey>/task/<int:task_id>')
api.add_resource(TaskListResource, '/api/<string:apikey>/tasks')

api.add_resource(MarkResource, '/api/<string:apikey>/mark/<int:mark_id>')
api.add_resource(MarkListResource, '/api/<string:apikey>/marks')


app.register_blueprint(app_blueprint, url_prefix="/app")
app.register_blueprint(auth_blueprint)
app.register_blueprint(about_blueprint, url_prefix='/about')
app.register_blueprint(other_blueprint)


@login_manager.user_loader
def user_loader(user_id):
    return users_utils.return_user(int(user_id))
