import os

import src.user_mgmt.authentication as auth
import src.user_mgmt.model as model


class UserMgmtController(object):
    """
    Login callback is used for testing only and should not be passed in production code
    """
    def __init__(self, user_manager, login_callback=None):
        self._user_manager = user_manager
        self._login_callback = self._get_login_callback(login_callback)


    def _get_login_callback(self, login_callback):
        if not login_callback:
            from flask_login import login_user
            return login_user
        return login_callback


    def register_user(self, username, plaintext_password, content_manager):
        salt = os.urandom(64)
        password_hash = auth.hash_password(plaintext_password, salt)
        user = model.User(username, password_hash, salt)
        self._user_manager.add_user(user, content_manager)
        self._do_login(user)
        return user


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