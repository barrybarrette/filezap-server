from io import BytesIO

from flask import Blueprint, request, send_file, render_template, redirect, jsonify, current_app
from flask_login import login_required, current_user

import src.config_manager as config_manager
import src.file_mgmt.content_managers.exceptions as content_manager_exceptions
import src.file_mgmt.controller as controller
import src.file_mgmt.datastore as datastore


blueprint = Blueprint(__name__, 'file_mgmt')


@blueprint.route('/', methods=['GET'])
@login_required
def list_files():
    ctrl = _get_controller()
    files = ctrl.get_files(current_user.username)
    return render_template('list_files.html', username=current_user.username, files=files)



@blueprint.route('/get_file', methods=['GET'])
@login_required
def get_file():
    content_id = request.args.get('contentId')
    if not content_id:
        return "Bad Request", 400
    ctrl = _get_controller()
    try:
        file = ctrl.get_file(content_id, current_user)
        return send_file(BytesIO(file.content), as_attachment=True, attachment_filename=file.filename)
    except content_manager_exceptions.ContentNotFoundError:
        ctrl.delete_file(content_id, current_user)
        return redirect('/')
    except datastore.FileNotFoundError:
        return redirect('/')



@blueprint.route('/delete_file', methods=['GET'])
@login_required
def delete_file():
    content_id = request.args.get('contentId')
    if not content_id:
        return "Bad Request", 400
    ctrl = _get_controller()
    ctrl.delete_file(content_id, current_user)
    return redirect('/')



@blueprint.route('/save_file', methods=['POST'])
@login_required
def save_file():
    file = request.files.get('file')
    ctrl = _get_controller()
    ctrl.save_file(file, current_user)
    return 'OK'



@blueprint.route('/from_url', methods=['POST'])
@login_required
def save_file_from_url():
    url = request.json.get('url')
    ctrl = _get_controller()
    ctrl.save_file_from(url, current_user)
    return 'OK'



@blueprint.route('/max_file_size', methods=['GET'])
def get_max_file_size():
    config = config_manager.get_config()
    return jsonify({'maxBytes': config.get('FILEZAP_MAX_FILE_SIZE')})



def _get_controller():
    config = config_manager.get_config()
    data_store = datastore.FileDataStore(config)
    content_manager = current_app.content_manager
    return controller.FileMgmtController(data_store, content_manager)



def register_blueprint(main_app):
    main_app.register_blueprint(blueprint)
