from flask import Blueprint, render_template, request

import src.config_manager as config_manager
import src.user_mgmt.datastore as datastore
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
        user = model.User(email, password)
        data_store = datastore.UserDataStore(config)
        try:
            data_store.add_user(user)
            return f'User {email} was added!'
        except datastore.DuplicateEmailError:
            return f'User {email} is already registered', 400
    return "Registrations are closed!", 400



def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)