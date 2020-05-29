import datetime

from flask import Blueprint
from flask import render_template, abort

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app.database.utils import session, tasks_utils, labels_utils
from .forms import AddMarkForm, AddTaskForm, EditMarkForm, EditTaskForm


blueprint = Blueprint('app', __name__, template_folder='templates')


@blueprint.route('/')
@login_required
def index_page():
    return redirect('all')


@blueprint.route('/apikey')
@login_required
def apikey_page():
    return render_template('app/apikey.html', apikey=current_user.apikey)


@blueprint.route('/all')
@login_required
def incoming_page():
    labels = labels_utils.get_labels(current_user.id)
    tasks = tasks_utils.get_tasks(current_user.id)

    params = {
        "marks": labels,
        "tasks": tasks,
        "day": datetime.date.today().day
    }

    return render_template('app/all.html', **params)


@blueprint.route('/today')
@login_required
def today_page():
    params = {
        "day": datetime.date.today().day,
        "tasks": tasks_utils.get_tasks_for_today(current_user.id),
        "marks": labels_utils.get_labels(current_user.id)
    }

    return render_template('app/today.html', **params)


@blueprint.route('/add_mark', methods=['GET', 'POST'])
@login_required
def add_mark_page():
    form = AddMarkForm()

    if form.validate_on_submit():
        if labels_utils.get_label(
                current_user.id, title=form.title.data) is None:
            labels_utils.create_label(current_user, form.title.data)
        return redirect('/app')

    return render_template('app/add_mark.html', form=form)


@blueprint.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task_page():
    form = AddTaskForm()
    form.marks.choices = [
        (str(mark.id), mark.title)
        for mark in labels_utils.get_labels(current_user.id)
    ]

    if form.validate_on_submit():
        labels = []

        for choice in form.marks.data:
            labels.append(
                labels_utils.get_label(current_user.id, label_id=int(choice)))

        finish_date = datetime.date(
            form.finish_date.data.year,
            form.finish_date.data.month,
            form.finish_date.data.day
        )

        tasks_utils.create_task(
            current_user.id, form.title.date, labels, finish_date
        )
        return redirect('/app')

    return render_template('app/add_task.html', form=form)


@blueprint.route('edit_mark/<int:label_id>', methods=['GET', 'POST'])
@login_required
def edit_mark_page(label_id):
    label = labels_utils.get_label(current_user.id, label_id=label_id)

    if label is None:
        abort(404)

    form = EditMarkForm()

    if form.validate_on_submit():
        if form.edit_button.data:
            label.title = form.title.data
        elif form.delete_button.data:
            session.delete(label)

        session.commit()
        return redirect('/app/all')

    form.title.process_data(label.title)
    return render_template('app/edit_mark.html', form=form)


@blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task_page(task_id):
    task = tasks_utils.get_task(current_user.id, task_id)

    if task is None:
        abort(404)

    form = EditTaskForm()

    form.labels.choices = [
        (str(label.id), label.title)
        for label in labels_utils.get_labels(current_user.id)
    ]

    if form.validate_on_submit():
        if form.edit_button.data:
            task.title = form.title.data

            labels = [
                labels_utils.get_label(current_user.id, label_id=int(label_id))
                for label_id in form.labels.data
            ]
            task.labels = labels

            task.finish_date = form.finish_date.data
        elif form.delete_button.data:
            session.delete(task)

        session.commit()
        return redirect('/app')

    form.title.process_data(task.title)
    form.finish_date.process_data(task.finish_date)

    return render_template('app/edit_task.html', form=form)


@blueprint.route('/show_tasks/<int:label_id>')
@login_required
def show_tasks_page(label_id):

    params = {
        "tasks": [
            task for task in tasks_utils.get_tasks(current_user.id)
            if any([label for label in task.labels if label.id == label_id])
        ],
        "title": labels_utils.get_label(
            current_user.id, label_id=label_id
        ).title,
        "marks": labels_utils.get_labels(current_user.id),
        "day": datetime.date.today().day
    }

    return render_template('app/tasks.html', **params)
