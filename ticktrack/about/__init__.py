from flask import Blueprint


blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/api')
def about_api():
    return 'ПУСТО'


@blueprint.route('/team')
def about_team():
    return 'ПУСТО'
