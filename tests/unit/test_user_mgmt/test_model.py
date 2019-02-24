import unittest

import src.user_mgmt.model as model



class TestUser(unittest.TestCase):

    def setUp(self):
        self.email = 'bob@bob.bob'
        self.password_hash = 'B0bIsGr8'
        self.user = model.User(self.email, self.password_hash)

    def test_uses_given_email_and_password(self):
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.password_hash, self.password_hash)


    def test_to_dict(self):
        as_dict = self.user.to_dict()
        expected = {
            'email': self.user.email,
            'password_hash': self.password_hash
        }
        self.assertEqual(as_dict, expected)


    def test_from_dict(self):
        user_dict = {'email': 'bob@bob.bob', 'password_hash': 'a_hash'}
        user = model.User.from_dict(user_dict)
        self.assertEqual(user.email, 'bob@bob.bob')
        self.assertEqual(user.password_hash, 'a_hash')