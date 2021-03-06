from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_mail import Mail

from . import database
database.global_init('app/db.sqlite')

from .database import models

from .about import blueprint as about_blueprint
from .other import blueprint as other_blueprint
from .api.task_resources import TaskResource, TaskListResource
from .api.mark_resources import LabelResource, LabelListResource

from . import config

app = Flask(__name__)
app.config.from_object(config.ProductionConfig)

mail = Mail()
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app) # noqa

from .auth import blueprint as auth_blueprint
from .main_app import blueprint as app_blueprint

api = Api(app) # noqa
api.add_resource(TaskResource, '/api/<string:apikey>/task/<int:task_id>')
api.add_resource(TaskListResource, '/api/<string:apikey>/tasks')

api.add_resource(LabelResource, '/api/<string:apikey>/mark/<int:label_id>')
api.add_resource(LabelListResource, '/api/<string:apikey>/marks')


app.register_blueprint(app_blueprint, url_prefix="/main_app")
app.register_blueprint(auth_blueprint)
app.register_blueprint(about_blueprint, url_prefix='/about')
app.register_blueprint(other_blueprint)


@login_manager.user_loader
def user_loader(user_id):
    session = database.create_session()
    return session.query(models.User).get(user_id)
