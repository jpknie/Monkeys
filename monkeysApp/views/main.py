import monkeysApp

from flask import Blueprint, make_response
from flask import render_template, request, make_response, flash, redirect, url_for

from sqlalchemy.exc import IntegrityError

from ..app import DbSession as db
from ..models import Monkey
from ..forms import MonkeyForm

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='../templates')


@main_blueprint.route('/', methods=['GET'])
def index():
    return "Hello world!"


@main_blueprint.route('/monkeys/add', methods=['GET', 'POST'])
def monkey_add():
    """
    Add new monkey to database
    """

    form = MonkeyForm()
    page_title = "Add monkey"
    if request.method == 'POST' and form.validate_on_submit():
        monkey = Monkey()
        form.populate_obj(monkey)
        try:
            db.add(monkey)
            db.commit()

        except IntegrityError, exc:
            reason = exc.message
            if reason.find('unique constraint'):
                flash('Email already in use, please use another email address!')
                db.rollback()
                return redirect(url_for('main_blueprint.monkey_add'))
        flash('New monkey added successfully')
        return redirect(url_for('main_blueprint.monkey_add'))
    return render_template('monkey_form.html', form_action='monkey_add', form=form, page_title=page_title)
