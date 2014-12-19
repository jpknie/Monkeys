import random

from flask import Blueprint, g, render_template, request, flash, redirect, url_for, session, make_response
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
@login_required
def index():
    """Browse user profiles"""
    page_title = "Browse profiles"
    monkeys = Monkey.query.all()
    return render_template('monkeys.html', page_title=page_title, profiles=monkeys)


@main_blueprint.route('/monkeys/add', methods=['GET', 'POST'])
@login_required
def monkey_add():
    """
    Add new monkey to database
    """
    if g.user.is_admin() != 1:
        flash('You are not allowed in here!')
        return redirect(url_for('main_blueprint.index'))

    form = MonkeyForm(request.form)
    page_title = "Add monkey"

    random_face = ['trollface.png', '9.jpg', 'monkey.png']

    if request.method == 'POST' and form.validate_on_submit():
        monkey = Monkey()
        face_num = random.randint(0, len(random_face) - 1)
        monkey.face_image = random_face[face_num]
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
    return render_template('monkey_form.html', form_action='/monkeys/add', form=form, page_title=page_title, form_edit=False)


@main_blueprint.route('/monkeys/friends', methods=['GET'])
@login_required
def monkey_friends():
    """Show list of friends of g.user"""
    page_title = "Your friends"
    me = g.user
    friends = me.all_friends
    return render_template('monkey_friends.html', friends=friends, page_title=page_title)


@main_blueprint.route('/monkeys/friend_requests', methods=['GET'])
@login_required
def monkey_friend_requests():
    """Get the list of pending friend requests"""
    page_title = "Friend requests"
    me = g.user
    frqs = me.friend_requests.all()
    return render_template('friend_requests.html', page_title=page_title, friend_requests=list(frqs))


@main_blueprint.route('/monkeys/profile', methods=['GET', 'POST'])
@login_required
def monkey_my_profile():
    """Get the profile of logged in user"""
    page_title = "Your profile"
    me = g.user

    form = MonkeyForm(request.form, obj=me)
    if form.validate_on_submit() and request.method == 'POST':
        monkey = Monkey.query.get(me.id)
        form.populate_obj(monkey)
        db.commit()
        return redirect(url_for('main_blueprint.monkey_my_profile'))

        return render_template('monkey_form.html', page_title=page_title, form=form, my_profile=True, monkey=me)
    return render_template('monkey_form.html', page_title=page_title, form=form, my_profile=True, monkey=me, form_edit=True)


@main_blueprint.route('/monkeys/profile/<int:monkey_id>', methods=['GET'])
@login_required
def monkey_show_profile(monkey_id):
    """Show profile with monkey id"""
    me = g.user
    monkey = Monkey.query.get(monkey_id)
    is_my_friend = monkey.is_friend(me)
    sent_friend_request = monkey.has_friend_request(me)
    rcvd_friend_request = me.has_friend_request(monkey)
    my_profile = False

    if me.id == monkey.id:
        my_profile = True

    if monkey is not None:
        return render_template('monkey_profile.html',
                               page_title=monkey.name,
                               my_profile=my_profile,
                               is_my_friend=is_my_friend,
                               profile=monkey,
                               sent_friend_request=sent_friend_request,
                               rcvd_friend_request=rcvd_friend_request)


@main_blueprint.route('/monkeys/remove_friend/<int:monkey_id>', methods=['GET'])
@login_required
def remove_friend(monkey_id):
    """Unfriend monkey"""
    me = g.user
    monkey = Monkey.query.filter_by(id=monkey_id).first()
    if monkey is not None:
        me.remove_friend(monkey)
        db.commit()
        return make_response("", 200)
    else:
        return make_response("", 400)


@main_blueprint.route('/monkeys/make_friend/<int:monkey_id>', methods=['GET'])
@login_required
def make_friend(monkey_id):
    """Be friends with monkey"""
    send_to = Monkey.query.filter_by(id=monkey_id).first()
    if send_to is not None:
        me = g.user
        if me.friend(send_to) is not False:
            db.commit()
            response = make_response("", 200)
        else:
            response = make_response("", 400)
        return response
    else:
        response = make_response("", 400)
        return response


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
    if g.user is not None:
        logout_user()
        flash('You were logged out')
        return redirect(url_for('main_blueprint.login'))
