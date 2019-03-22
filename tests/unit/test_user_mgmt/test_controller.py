import unittest

import src.user_mgmt.authentication as auth
import src.user_mgmt.controller as controller


class TestUserControllerBase(unittest.TestCase):

    def setUp(self):
        self.user_manager = UserManagerDouble()
        self.content_manager = ContentManagerDummy()
        self.controller = controller.UserMgmtController(self.user_manager, self.content_manager, self.login_callback)
        self.password = 'plain_password'
        self.user = self.controller.register_user('bob', self.password)


    # Helper
    def login_callback(self, user):
        self.logged_in_user = user




class TestRegisterUser(TestUserControllerBase):

    def test_adds_user_to_user_manager(self):
        self.assertIs(self.user_manager.invoked_user, self.user)


    def test_passes_content_manager_to_user_manager(self):
        self.assertIs(self.user_manager.invoked_content_manager, self.content_manager)


    def test_generates_salt(self):
        self.assertIsInstance(self.user_manager.invoked_user.salt, bytes)


    def test_hashes_password(self):
        hashed_password = auth.hash_password(self.password, self.user_manager.invoked_user.salt)
        self.assertEqual(self.user_manager.invoked_user.password_hash, hashed_password)


    def test_authenticates_and_logs_user_in(self):
        self.assertTrue(self.logged_in_user.is_authenticated)




class TestLoginUser(TestUserControllerBase):

    def setUp(self):
        super(TestLoginUser, self).setUp()
        self.logged_in_user = None  # Clear invocation from super.setUp


    def test_login_user_raises_exception_if_user_does_not_exist(self):
        with self.assertRaises(controller.InvalidCredentialsError):
            self.controller.login_user('<invalid_user>', self.password)
        self.assertIsNone(self.logged_in_user)


    def test_login_user_raises_exception_if_password_is_incorrect(self):
        with self.assertRaises(controller.InvalidCredentialsError):
            self.controller.login_user('bob', '<invalid password>')
        self.assertIsNone(self.logged_in_user)


    def test_login_user_sets_user_authentication_value_and_invokes_callback(self):
        self.controller.register_user('bob', self.password)
        self.controller.login_user('bob', self.password)
        self.assertTrue(self.logged_in_user.is_authenticated)




class TestDeleteUser(TestUserControllerBase):


    def test_raises_exception_if_password_is_incorrect(self):
        with self.assertRaises(controller.InvalidCredentialsError):
            self.controller.delete_user(self.logged_in_user, '<invalid password>')


    def test_invokes_user_manager(self):
        self.user_manager.invoked_user = None # Clear invocation from super.setUp
        self.user_manager.invoked_content_manager = None  # Clear invocation from super.setUp
        self.controller.delete_user(self.logged_in_user, self.password)
        self.assertIs(self.user_manager.invoked_user, self.logged_in_user)
        self.assertIs(self.user_manager.invoked_content_manager, self.content_manager)



class UserManagerDouble(object):

    def __init__(self):
        self.invoked_user = None
        self.invoked_content_manager = None
        self._users = {}


    def __contains__(self, username):
        return username in self._users


    def add_user(self, user, content_manager):
        self.invoked_user = user
        self.invoked_content_manager = content_manager
        self._users[user.username] = user


    def get_user(self, username):
        return self._users.get(username)


    def delete_user(self, user, content_manager):
        self.invoked_user = user
        self.invoked_content_manager = content_manager


class ContentManagerDummy(object): pass
