import os

import src.user_mgmt.authentication as auth
import src.user_mgmt.model as model


class UserMgmtController(object):

    def __init__(self, user_manager):
        self._user_manager = user_manager


    def register_user(self, email, plaintext_password):
        salt = os.urandom(64)
        password_hash = auth.hash_password(plaintext_password, salt)
        user = model.User(email, password_hash, salt)
        self._user_manager.add_user(user)


    def login_user(self, email, password, callback):
        user = self._user_manager.get_user(email)
        if not user:
            raise InvalidCredentialsError()
        password_hash = auth.hash_password(password, user.salt)
        if password_hash != user.password_hash:
            raise InvalidCredentialsError()
        user.is_authenticated = True
        callback(user)





class InvalidCredentialsError(Exception):
    pass