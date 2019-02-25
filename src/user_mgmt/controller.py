import os

import src.user_mgmt.authentication as auth
import src.user_mgmt.model as model


class UserMgmtController(object):

    def __init__(self, user_manager, login_callback=None):
        self._user_manager = user_manager
        if login_callback:
            self._login_callback = login_callback
        else:
            from flask_login import login_user
            self._login_callback = login_user


    def register_user(self, username, plaintext_password):
        salt = os.urandom(64)
        password_hash = auth.hash_password(plaintext_password, salt)
        user = model.User(username, password_hash, salt)
        self._user_manager.add_user(user)
        self._do_login(user)


    def login_user(self, username, password):
        user = self._user_manager.get_user(username)
        if not user:
            raise InvalidCredentialsError()
        password_hash = auth.hash_password(password, user.salt)
        if password_hash != user.password_hash:
            raise InvalidCredentialsError()
        self._do_login(user)


    def _do_login(self, user):
        user.is_authenticated = True
        self._login_callback(user)




class InvalidCredentialsError(Exception):
    pass