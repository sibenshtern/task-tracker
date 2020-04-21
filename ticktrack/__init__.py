import os

from flask import Flask
from flask_login import LoginManager

from ticktrack.database import utils

from ticktrack.app import blueprint as app_blueprint
from ticktrack.auth import blueprint as auth_blueprint
from ticktrack.other import blueprint as other_blueprint


app = Flask(__name__)
app.secret_key = os.urandom(16)
app.max_id = utils.search_max_id()

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(app_blueprint, url_prefix="/app")
app.register_blueprint(auth_blueprint)
app.register_blueprint(other_blueprint)


@login_manager.user_loader
def user_loader(user_id):
    return utils.return_user(int(user_id))


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(port=port, debug=True)
