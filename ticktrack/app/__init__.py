from datetime import datetime

from flask import Blueprint
from flask import render_template

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ticktrack.database import utils as db_utils
from ticktrack.app.forms import AddMarkForm

blueprint = Blueprint('app', __name__, template_folder='templates')


@blueprint.route('/')
@login_required
def index_page():
    return redirect('all')


@blueprint.route('/all')
@login_required
def incoming_page():
    return render_template(
        'app/all.html', day=datetime.now().day, title="Все задачи",
        marks=db_utils.return_marks(current_user.id),
        tasks=db_utils.return_all_tasks(current_user.id)
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


@blueprint.route('/add_mark')
@login_required
def add_mark():
    form = AddMarkForm()
    return render_template('app/add_mark.html', form=form)
