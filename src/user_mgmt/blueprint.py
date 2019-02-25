from flask import Blueprint, render_template, request, redirect, current_app
from flask_login import login_required, login_user

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
        email = request.form.get('email')
        password = request.form.get('password')
        user_manager = current_app.user_manager
        user_mgmt_controller = controller.UserMgmtController(user_manager)
        try:
            user_mgmt_controller.register_user(email, password)
            return f'User {email} was added!'
        except model.DuplicateUserError:
            return f'User {email} is already registered', 400
    return "Registrations are closed!", 400



@blueprint.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')


@blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user_manager = current_app.user_manager
    user_mgmt_controller = controller.UserMgmtController(user_manager)
    try:
        user_mgmt_controller.login_user(email, password, login_user)
        return redirect('/')
    except controller.InvalidCredentialsError:
        return render_template('login.html', msg='Invalid credentials!')


# Temporary endpoint for login testing - will be deleted
@blueprint.route('/', methods=['GET'])
@login_required
def protected_resource():
    return "Congratulations you are logged in!"



def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)