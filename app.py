from flask import Flask

import src.user_mgmt.blueprint as user_mgmt_blueprint


class FileZapServer(Flask):

    def __init__(self):
        super(FileZapServer, self).__init__(__name__)
        user_mgmt_blueprint.register_blueprint(self)