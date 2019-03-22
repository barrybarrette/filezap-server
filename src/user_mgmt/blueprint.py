from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, logout_user, current_user

import src.config_manager as config_manager
import src.user_mgmt.controller as controller
import src.user_mgmt.model as model


blueprint = Blueprint(__name__, 'user_mgmt')
config = config_manager.get_config()


@blueprint.route('/register', methods=['GET'])
def register_view():
    if config.get('USER_REGISTRATION_ENABLED'):
        return render_template('register.html')
    return render_template('no_register.html')


@blueprint.route('/register', methods=['POST'])
def register_post():
    if config.get('USER_REGISTRATION_ENABLED'):
        username = request.form.get('username').strip().lower()
        if not username.isalpha():
            return render_template('register.html', msg=f'Invalid username. Enter only letters, no numbers or symbols')
        password = request.form.get('password')
        user_mgmt_controller = _get_controller()
        try:
            user_mgmt_controller.register_user(username, password)
            return redirect('/')
        except model.DuplicateUserError:
            return render_template('register.html', msg=f'User {username} is already registered')
    return "Registrations are closed!", 400



@blueprint.route('/login', methods=['GET'])
def login_view(msg=None):
    return render_template('login.html', msg=msg)


@blueprint.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username').strip().lower()
    password = request.form.get('password')
    user_mgmt_controller = _get_controller()
    try:
        user_mgmt_controller.login_user(username, password)
        return redirect('/')
    except controller.InvalidCredentialsError:
        return render_template('login.html', msg='Invalid credentials!')


@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    _do_logout()
    return render_template('login.html', msg='You have been logged out.')


@blueprint.route('/deleteAccount', methods=['GET'])
def get_delete_account():
    return render_template('delete_account.html')


@blueprint.route('/deleteAccount', methods=['POST'])
def post_delete_account():
    user_mgmt_controller = _get_controller()
    password = request.form.get('password')
    try:
        user_mgmt_controller.delete_user(current_user, password)
        _do_logout()
        return render_template('login.html', msg='Your account and all of your files have been deleted.')
    except controller.InvalidCredentialsError:
        return render_template('delete_account.html', msg='Invalid password')


def _get_controller():
    user_manager = current_app.user_manager
    content_manager = current_app.content_manager
    return controller.UserMgmtController(user_manager, content_manager)


def _do_logout():
    current_user.is_authenticated = False
    logout_user()



def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)