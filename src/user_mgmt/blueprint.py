from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, logout_user, current_user

import src.config_manager as config_manager
import src.file_mgmt.content_managers as content_managers
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
        user_manager = current_app.user_manager
        user_mgmt_controller = controller.UserMgmtController(user_manager)
        content_manager = content_managers.BackBlazeContentManager()
        try:
            user_mgmt_controller.register_user(username, password, content_manager)
            return redirect('/')
        except model.DuplicateUserError:
            return render_template('register.html', msg=f'User {username} is already registered')
    return "Registrations are closed!", 400



@blueprint.route('/login', methods=['GET'])
def login_view(msg=None):
    return render_template('login.html', msg=msg)


@blueprint.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user_manager = current_app.user_manager
    user_mgmt_controller = controller.UserMgmtController(user_manager)
    try:
        user_mgmt_controller.login_user(username, password)
        return redirect('/')
    except controller.InvalidCredentialsError:
        return render_template('login.html', msg='Invalid credentials!')


@blueprint.route('/logout', methods=['GET'])
@login_required
def logout():
    current_user.is_authenticated = False
    logout_user()
    return render_template('login.html', msg='You have been logged out.')



def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)