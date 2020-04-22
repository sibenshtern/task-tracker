from datetime import datetime

from flask import Blueprint
from flask import render_template

from flask_login import login_required, current_user
from ticktrack.database import utils as db_utils

blueprint = Blueprint('app', __name__, template_folder='templates')


@blueprint.route('/incoming')
@login_required
def incoming_page():
    return render_template(
        'app/incoming.html', day=datetime.now().day, title="Входящие",
        marks=db_utils.return_marks(current_user.id)
    )


@blueprint.route('/today')
@login_required
def today_page():
    tasks = db_utils.return_today_tasks(current_user.id)

    return render_template(
        'app/today.html', day=datetime.now().day, title="Сегодня", tasks=tasks,
        marks=db_utils.return_marks(current_user.id)
    )


@blueprint.route('/next_week')
@login_required
def next_week_page():
    return render_template(
        'app/next_week.html', day=datetime.now().day, title="Следующая неделя",
        marks=db_utils.return_marks(current_user.id)
    )

