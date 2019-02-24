from flask import Blueprint, render_template, request

import src.user_mgmt.datastore as datastore
import src.user_mgmt.model as model


blueprint = Blueprint(__name__, 'user_mgmt')


@blueprint.route('/register', methods=['GET'])
def register_view():
    return render_template('register.html')


@blueprint.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = model.User(email, password)
    data_store = datastore.UserDataStore()
    try:
        data_store.add_user(user)
        return f'User {email} was added!'
    except datastore.DuplicateEmailError:
        return f'User {email} is already registered, reset password?'


def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)