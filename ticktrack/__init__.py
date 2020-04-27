import os

from flask import Flask
from flask_login import LoginManager
from flask_restful import Api

from ticktrack.database import users_utils

from ticktrack.app import blueprint as app_blueprint
from ticktrack.auth import blueprint as auth_blueprint
from ticktrack.about import blueprint as about_blueprint
from ticktrack.other import blueprint as other_blueprint
from ticktrack.api import TaskResource


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.max_id = users_utils.search_max_id_in_users()

login_manager = LoginManager()
login_manager.init_app(app) # noqa

api = Api(app) # noqa
api.add_resource(TaskResource, '/api/<string:apikey>/task/<int:task_id>')


app.register_blueprint(app_blueprint, url_prefix="/app")
app.register_blueprint(auth_blueprint)
app.register_blueprint(about_blueprint, url_prefix='/about')
app.register_blueprint(other_blueprint)


@login_manager.user_loader
def user_loader(user_id):
    return users_utils.return_user(int(user_id))
