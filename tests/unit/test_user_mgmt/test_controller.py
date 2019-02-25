import unittest

import src.user_mgmt.authentication as auth
import src.user_mgmt.controller as controller


class TestUserMgmtController(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManagerDouble()
        self.controller = controller.UserMgmtController(self.user_manager, self.login_callback)
        self.controller.register_user('bob', 'plain_password')


    def test_register_user_adds_user_to_data_store(self):
        self.assertIsNotNone(self.user_manager.invoked_user)


    def test_register_user_uses_specified_username(self):
        self.assertEqual(self.user_manager.invoked_user.username, 'bob')


    def test_register_user_generates_salt(self):
        self.assertIsInstance(self.user_manager.invoked_user.salt, bytes)


    def test_register_user_hashes_password(self):
        hashed_password = auth.hash_password('plain_password', self.user_manager.invoked_user.salt)
        self.assertEqual(self.user_manager.invoked_user.password_hash, hashed_password)


    def test_register_user_authenticates_and_logs_user_in(self):
        self.assertTrue(self.login_callback_invoked_user.is_authenticated)


    def test_login_user_raises_exception_if_user_does_not_exist(self):
        self.login_callback_invoked_user = None # Clearing invocation from registering a user
        with self.assertRaises(controller.InvalidCredentialsError):
            self.controller.login_user('<invalid_user>', 'password')
        self.assertIsNone(self.login_callback_invoked_user)


    def test_login_user_raises_exception_if_password_is_incorrect(self):
        self.login_callback_invoked_user = None # Clearing invocation from registering a user
        with self.assertRaises(controller.InvalidCredentialsError):
            self.controller.login_user('bob', '<invalid password>')
        self.assertIsNone(self.login_callback_invoked_user)


    def test_login_user_sets_user_authentication_value_and_invokes_callback(self):
        self.controller.login_user('bob', 'plain_password')
        self.assertTrue(self.login_callback_invoked_user.is_authenticated)


    # Helper
    def login_callback(self, user):
        self.login_callback_invoked_user = user


class UserManagerDouble(object):

    def __init__(self):
        self.invoked_user = None
        self._users = {}


    def add_user(self, user):
        self.invoked_user = user
        self._users[user.username] = user


    def get_user(self, username):
        return self._users.get(username)
























