import base64
import os
import unittest

import src.user_mgmt.model as model



class TestUserBase(unittest.TestCase):

    def setUp(self):
        self.username = 'bob'
        self.hashed_password = 'B0bIsGr8'
        self.salt = os.urandom(32)
        self.content_credentials = 'app_id:secret_key'
        self.user = model.User(self.username, self.hashed_password, self.salt, self.content_credentials)



class TestUserImplementsFlaskLoginInterface(TestUserBase):

    def test_user_is_not_authenticated_when_created(self):
        self.assertEqual(self.user.is_authenticated, False)

    def test_always_returns_user_is_active(self):
        self.assertEqual(self.user.is_active, True)

    def test_always_returns_user_is_not_anonymous(self):
        self.assertEqual(self.user.is_anonymous, False)

    def test_implements_get_id(self):
        self.assertEqual(self.user.get_id(), self.user.username)



class TestUser(TestUserBase):

    def test_uses_given_attributes(self):
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.password_hash, self.hashed_password)
        self.assertEqual(self.user.salt, self.salt)


    def test_content_credentials_default_to_none_if_not_provided(self):
        """
        The idea behind this behavior is that not all content managers will
        necessarily have authentication, so we want to make it optional
        """
        user = model.User(self.username, self.hashed_password, self.salt)
        self.assertIsNone(user.content_credentials)


    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict, self.get_user_dict())


    def test_from_dict(self):
        user = model.User.from_dict(self.get_user_dict())
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.password_hash, self.hashed_password)
        self.assertEqual(user.salt, self.salt)
        self.assertEqual(user.content_credentials, self.content_credentials)




    # Helper
    def get_user_dict(self):
        b64_encoded_salt = base64.b64encode(self.salt).decode()
        return {
            'username': self.username,
            'password_hash': self.hashed_password,
            'salt': b64_encoded_salt,
            'content_credentials': self.content_credentials
        }



class TestUserManagerBase(unittest.TestCase):

    def setUp(self):
        self.data_store = DataStoreDouble()
        self.content_manager = ContentManagerDouble()
        self.user_manager = model.UserManager(self.data_store)



class TestUserManager(TestUserManagerBase):

    def test_no_users_registered_on_creation(self):
        self.assertEqual(self.user_manager.user_count, 0)



class TestAddUser(TestUserManagerBase):

    def setUp(self):
        super(TestAddUser, self).setUp()
        self.user = model.User('bob', 'bob_password', b'salt')
        self.user_manager.add_user(self.user, self.content_manager)


    def test_can_add_user(self):
        self.assertIs(self.data_store.added_user, self.user)
        self.assertEqual(self.user_manager.user_count, 1)


    def test_adding_user_with_duplicate_username_raises_exception(self):
        self.content_manager.invoked_user = None # Clear invocation from setUp()
        with self.assertRaises(model.DuplicateUserError):
            self.user_manager.add_user(self.user, self.content_manager)
        self.assertIsNone(self.content_manager.invoked_user)


    def test_generates_content_credentials_for_user(self):
        self.assertIs(self.content_manager.invoked_user, self.user)





class TestGetUser(TestUserManagerBase):

    def test_can_get_user_by_username(self):
        username = 'bob'
        user = model.User(username, 'bob_password', b'salt')
        self.user_manager.add_user(user, self.content_manager)
        loaded_user = self.user_manager.get_user(username)
        self.assertIs(loaded_user, user)


    def test_can_load_users_from_data_store(self):
        self.user_manager.load_users()
        self.assertEqual(self.user_manager.user_count, 2)


    def test_loading_users_from_data_store_does_not_try_to_add_them_back_to_data_store(self):
        self.user_manager.load_users()
        self.assertIsNone(self.data_store.added_user)




class DataStoreDouble(object):

    def __init__(self):
        self.added_user = None


    def get_all_users(self):
        return [
            model.User('username1', 'password1', b'salt1'),
            model.User('username2', 'password2', b'salt2')
        ]


    def add_user(self, user):
        self.added_user = user



class ContentManagerDouble(object):

    def __init__(self):
        self.invoked_user = None

    def generate_credentials(self, user):
        self.invoked_user = user
