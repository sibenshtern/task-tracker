from flask import Blueprint
from flask import render_template


blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/api')
def about_api():
    return 'ПУСТО'


@blueprint.route('/team')
def about_team():
    return render_template('about/team.html')
