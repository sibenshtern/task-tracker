from os import urandom

from flask import Flask

app = Flask(__name__)
app.secret_key = urandom(16)
