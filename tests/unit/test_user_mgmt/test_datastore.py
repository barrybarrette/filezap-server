import unittest

import src.user_mgmt.datastore as datastore
import src.user_mgmt.model as model


class TestUserDataStore(unittest.TestCase):

    def setUp(self):
        self.dynamodb = DynamoDbDouble()
        config = {'USER_DB_TABLE': 'the_user_table'}
        self.data_store = datastore.UserDataStore(config, self.dynamodb)


    def test_adds_user_to_dynamo_db(self):
        user = model.User('realuser@gmail.com', 'a_password', b'salt')
        self.data_store.add_user(user)
        self.assertEqual(self.dynamodb.invoked_put_item, user.to_dict())


    def test_uses_configured_table_name(self):
        self.assertEqual(self.dynamodb.invoked_table, 'the_user_table')


    def test_can_get_all_users(self):
        users = self.data_store.get_all_users()
        self.assertTrue(self.dynamodb.get_all_invoked)
        self.assertEqual(len(users), 2)
        for user in users:
            self.assertIsInstance(user, model.User)


class DynamoDbDouble(object):

    def __init__(self):
        self._users = [
            {'username': 'bob', 'password_hash': 'a_hash', 'salt': 'somesalt='},
            {'username': 'bob2', 'password_hash': 'a_hash', 'salt': 'somesalt='}
        ]
        self.invoked_put_item = None
        self.invoked_table = None
        self.get_all_invoked = False


    def Table(self, table_name):
        self.invoked_table = table_name
        return self


    def put_item(self, Item):
        self.invoked_put_item = Item


    def scan(self):
        self.get_all_invoked = True
        return {'Items': self._users}