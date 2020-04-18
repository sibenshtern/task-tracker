import os

from flask import Flask

from ticktrack.auth import blueprint as auth_blueprint
from ticktrack.other import blueprint as other_blueprint


app = Flask(__name__)
app.secret_key = os.urandom(16)

app.register_blueprint(auth_blueprint)
app.register_blueprint(other_blueprint)


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(port=port, debug=True)
