import unittest

import src.user_mgmt.datastore as datastore
import src.user_mgmt.model as model


class TestUserDataStore(unittest.TestCase):

    def setUp(self):
        self.dynamodb = DynamoDbDouble()
        config = {'USER_DB_TABLE': 'the_user_table'}
        self.data_store = datastore.UserDataStore(config, self.dynamodb)
        self.user = model.User('realuser', 'a_password', b'salt')
        self.data_store.add_user(self.user)


    def test_uses_configured_table_name(self):
        self.assertEqual(self.dynamodb.invoked_table, 'the_user_table')


    def test_adds_user_to_dynamo_db(self):
        self.assertEqual(self.dynamodb.invoked_put_item, self.user.to_dict())


    def test_get_user_queries_on_correct_key(self):
        self.data_store.get_user('bob')
        self.assertEqual(self.dynamodb.invoked_get_key, {'username': 'bob'})



    def test_returns_none_if_user_not_in_db(self):
        user = self.data_store.get_user('<invalid user>')
        self.assertIsNone(user)


    def test_returns_user_if_user_is_in_db(self):
        user = self.data_store.get_user('realuser')
        self.assertIsInstance(user, model.User)


    def test_delete_user_queries_on_correct_key(self):
        self.data_store.delete_user(self.user.username)
        self.assertEqual(self.dynamodb.invoked_delete_key, {'username': self.user.username})




class DynamoDbDouble(object):

    def __init__(self):
        self.invoked_put_item = None
        self.invoked_get_key = None
        self.invoked_delete_key = None
        self.invoked_table = None


    def Table(self, table_name):
        self.invoked_table = table_name
        return self


    def put_item(self, Item):
        self.invoked_put_item = Item


    def get_item(self, Key):
        self.invoked_get_key = Key
        if Key.get('username') == '<invalid user>':
            return {}
        return {'Item': {'username': 'bob', 'password_hash': 'a_hash', 'salt': 'somesalt='}}


    def delete_item(self, Key):
        self.invoked_delete_key = Key