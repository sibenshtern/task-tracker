import os

from ticktrack import app


if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(port=port, debug=True)
