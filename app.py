import os

from gevent.pywsgi import WSGIServer

from app import app


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()
