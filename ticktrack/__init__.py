import os

from flask import Flask

app = Flask(__name__)
app.secret_key = os.urandom(16)


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(port=port)
