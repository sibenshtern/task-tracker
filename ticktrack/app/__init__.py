from datetime import datetime

from flask import Blueprint
from flask import render_template, abort

from flask_login import login_required, current_user
from werkzeug.utils import redirect

from ticktrack.database import tasks_utils, marks_utils
from ticktrack.app.forms import AddMarkForm, AddTaskForm, EditMarkForm, \
    EditTaskForm

blueprint = Blueprint('app', __name__, template_folder='templates')


@blueprint.route('/')
@login_required
def index_page():
    return redirect('all')


@blueprint.route('/apikey')
@login_required
def apikey_page():
    return render_template(
        'app/apikey.html', apikey=current_user.return_apikey(),
        current_user=current_user
    )


@blueprint.route('/all')
@login_required
def incoming_page():
    return render_template(
        'app/all.html', day=datetime.now().day, title="Все задачи",
        marks=marks_utils.return_marks(current_user.id),
        tasks=tasks_utils.return_all_tasks(current_user.id),
        current_user=current_user
    )


@blueprint.route('/today')
@login_required
def today_page():
    tasks = tasks_utils.return_today_tasks(current_user.id)

    return render_template(
        'app/today.html', day=datetime.now().day, title="Сегодня", tasks=tasks,
        marks=marks_utils.return_marks(current_user.id),
        current_user=current_user
    )


@blueprint.route('/next_week')
@login_required
def next_week_page():
    return render_template(
        'app/next_week.html', day=datetime.now().day, title="Следующая неделя",
        marks=marks_utils.return_marks(current_user.id),
        current_user=current_user
    )


@blueprint.route('/add_mark', methods=['GET', 'POST'])
@login_required
def add_mark_page():
    form = AddMarkForm()

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/add_mark.html', form=form, title="Добавить метку",
                current_user=current_user
            )

        if marks_utils.return_mark(
                current_user.id, title=form.title.data
                ) is None:
            marks_utils.create_mark(form.title.data)
        return redirect('/app')

    return render_template(
        'app/add_mark.html', form=form, title="Добавить метку",
        current_user=current_user
    )


@blueprint.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task_page():
    form = AddTaskForm()
    form.marks.choices = [
        (str(mark.id), mark.title) for mark in current_user.marks
    ]

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/add_task.html', form=form, title="Добавить задачу",
                current_user=current_user
            )
        marks = [
            marks_utils.return_mark(current_user.id, int(task_id))
            for task_id in form.marks.data
        ]
        finish_date = datetime(
            form.finish_date.data.year, form.finish_date.data.month,
            form.finish_date.data.day
        )

        tasks_utils.create_task(form.title.data, marks, finish_date)
        return redirect('/app')

    return render_template(
        'app/add_task.html', form=form, title="Добавить задачу",
        current_user=current_user
    )


@blueprint.route('edit_mark/<int:mark_id>', methods=['GET', 'POST'])
@login_required
def edit_mark_page(mark_id):
    if marks_utils.return_mark(current_user.id, mark_id) is None:
        abort(404)

    form = EditMarkForm()
    mark = marks_utils.return_mark(current_user.id, mark_id)

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/edit_mark.html', form=form, current_user=current_user
            )

        if form.edit_button.data:
            for mark in current_user.marks:
                if mark.id == mark_id:
                    mark.title = form.title.data
            current_user.save()
            # Здесь я усложняю код, когда ищу марку через цикл, но это
            # вынужденная мера. У меня хоть и есть функция, которая
            # возвращает метку, но она возвращает другой объект, и из-за
            # этого библиотека pymodm не срабатывает должным образом
            # Во всех подобных случаях, идентичная проблема.
        elif form.delete_button.data:
            for index in range(len(current_user.marks)):
                # Проверяю, потому что метка может удалиться и
                # тогда выпадет исключение IndexError
                if index < len(current_user.marks):
                    if current_user.marks[index].id == mark_id:
                        if len(current_user.marks) > 1:
                            del current_user.marks[index]
                        else:
                            del current_user.marks

            current_user.save()
        return redirect('/app/all')

    form.title.process_data(mark.title)
    return render_template(
        'app/edit_mark.html', form=form, current_user=current_user
    )


@blueprint.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task_page(task_id):
    if tasks_utils.return_task(current_user.id, task_id) is None:
        abort(404)

    form = EditTaskForm()
    form.marks.choices = [
        (str(mark.id), mark.title) for mark in current_user.marks
    ]

    if form.validate_on_submit():
        if not form.validate():
            return render_template(
                'app/edit_task.html', form=form, current_user=current_user
            )

        # проверяем, что кнопка "изменить метку" нажата
        if form.edit_submit.data:
            for task in current_user.tasks:
                if task.id == task_id:
                    task.title = form.title.data

                    print(form.marks.data)
                    marks = [
                        marks_utils.return_mark(current_user.id, int(task_id))
                        for task_id in form.marks.data
                    ]
                    if len(marks) > 0:
                        task.marks = marks
                    else:
                        del task.marks

                    task.finish_date = datetime(
                        form.finish_date.data.year,
                        form.finish_date.data.month,
                        form.finish_date.data.day
                    )
        # проверяем, что нажата кнопка "удалить метку"
        elif form.delete_submit.data:
            for index in range(len(current_user.tasks)):
                if index < len(current_user.tasks):
                    if current_user.tasks[index].id == task_id:
                        if len(current_user.tasks) > 1:
                            del current_user.tasks[index]
                        else:
                            del current_user.tasks

        current_user.save()
        return redirect('/app')

    task = tasks_utils.return_task(current_user.id, task_id)

    form.title.process_data(task.title)
    form.finish_date.process_data(task.finish_date)

    return render_template(
        'app/edit_task.html', form=form, current_user=current_user
    )


@blueprint.route('/show_tasks/<int:mark_id>')
@login_required
def show_tasks_page(mark_id):
    tasks = [
        task for task in current_user.tasks
        if any([mark for mark in task.marks if mark.id == mark_id])
    ]

    return render_template(
        'app/tasks.html', tasks=tasks,
        title=marks_utils.return_mark(current_user.id, mark_id).title,
        marks=marks_utils.return_marks(current_user.id),
        current_user=current_user, day=datetime.now().day
    )
