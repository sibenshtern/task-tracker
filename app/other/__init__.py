from flask import Blueprint
from flask import render_template


blueprint = Blueprint('other', __name__, template_folder='templates')


@blueprint.route('/')
def index_page():
    return render_template('index.html', title="NegotiumTracker")
