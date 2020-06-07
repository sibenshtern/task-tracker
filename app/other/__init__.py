from flask import Blueprint
from flask import render_template

from flask_login import current_user
from werkzeug.utils import redirect


blueprint = Blueprint('other', __name__, template_folder='templates')


@blueprint.route('/')
def index_page():
    if current_user.is_authenticated:
        return redirect('/main_app')
    return render_template('index.html', title="TickTrack")
