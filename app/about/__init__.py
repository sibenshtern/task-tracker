from flask import Blueprint
from flask import render_template, request


blueprint = Blueprint('about', __name__, template_folder='templates')


@blueprint.route('/api')
def about_api():
    return render_template('about/api.html', host=request.url_root)


@blueprint.route('/team')
def about_team():
    return render_template('about/team.html')
