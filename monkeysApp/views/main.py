from flask import Blueprint, g, render_template, request, flash, redirect, url_for, session
from flask.ext.login import current_user, login_required, logout_user

from sqlalchemy.exc import IntegrityError

from ..app import login_manager, DbSession as db
from ..models import Monkey
from ..forms import MonkeyForm, LoginForm

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='../templates')


@login_manager.user_loader
def load_user(user_id):
    return Monkey.query.get(int(user_id))


@main_blueprint.before_request
def before_request():
    g.user = current_user


@main_blueprint.route('/', methods=['GET'])
def index():
    """Show something common for all (statuses?) on the index page"""
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


@login_required
@main_blueprint.route('/monkeys/friends', methods=['GET'])
def monkey_friends():
    """Show list of friends of g.user"""
    pass


@login_required
@main_blueprint.route('/monkeys/friend_requests', methods=['GET'])
def monkey_friend_requests():
    """Get the list of pending friend requests"""
    pass


@login_required
@main_blueprint.route('/monkeys/profile', methods=['GET'])
def monkey_my_profile():
    """Get the profile of logged in user"""
    pass


@login_required
@main_blueprint.route('/monkeys/profile/<int:monkey_id>', methods=['GET'])
def monkey_show_profile(monkey_id):
    """Show profile with monkey id"""
    pass


@login_required
@main_blueprint.route('/monkeys/friend_request/<int:monkey_id>', methods=['GET'])
def send_friend_request(monkey_id):
    """Send a friend request from g.user to monkey with monkey_id"""
    pass


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login with user email and password"""
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = Monkey.query.filter_by(email=form.login_name.data).first()
        if user and (user.password == form.password.data):
            session['user_id'] = user.id
            flash('Welcome %s' % user.email)
            return redirect(url_for('main_blueprint.index'))
        flash('Wrong email or password', 'error-message')
    return render_template('login.html', form=form)


@main_blueprint.route('/logout')
@login_required
def logout():
    """Logout currently authenticated user"""
    logout_user()
    flash('You were logged out')
    return redirect(url_for('main_blueprint.login'))
