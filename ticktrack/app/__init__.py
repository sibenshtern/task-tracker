from datetime import datetime

from flask import Blueprint
from flask import render_template

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ticktrack.database.models import Mark
from ticktrack.database import utils as db_utils
from ticktrack.app.forms import AddMarkForm, AddTaskForm

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
        marks=db_utils.return_marks(current_user.id), current_user=current_user
    )


@blueprint.route('/add_mark', methods=['GET', 'POST'])
@login_required
def add_mark():
    form = AddMarkForm()

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/add_mark.html', form=form, title="Добавить метку",
                current_user=current_user
            )
        db_utils.create_mark(form.title.data)
        return redirect('/app')

    return render_template(
        'app/add_mark.html', form=form, title="Добавить метку",
        current_user=current_user
    )


@blueprint.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = AddTaskForm()
    form.marks.choices = [(str(mark.id), mark.title) for mark in current_user.marks]

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/add_task.html', form=form, title="Добавить задачу",
                current_user=current_user
            )
        marks = [db_utils.return_mark(current_user.id, int(task_id))
                 for task_id in form.marks.data]
        finish_date = datetime(
            form.finish_date.data.year, form.finish_date.data.month,
            form.finish_date.data.day
        )

        db_utils.create_task(form.title.data, marks, finish_date)
        return redirect('/app')

    return render_template(
        'app/add_task.html', form=form, title="Добавить задачу",
        current_user=current_user
    )

