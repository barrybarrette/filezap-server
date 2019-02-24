import unittest

import src.user_mgmt.datastore as datastore
import src.user_mgmt.model as model


class TestUserDataStore(unittest.TestCase):

    def setUp(self):
        self.dynamodb = DynamoDbDouble()
        self.data_store = datastore.UserDataStore(self.dynamodb)


    def test_raises_if_adding_user_and_email_already_exists(self):
        with self.assertRaises(datastore.DuplicateEmailError):
            self.data_store.add_user(model.User('bob@bob.bob', 'a_password'))


    def test_adds_user_to_dynamo_db_if_email_does_not_exist(self):
        user = model.User('realuser@gmail.com', 'a_password')
        self.data_store.add_user(user)
        self.assertEqual(self.dynamodb.invoked_put_item, user.to_dict())






class DynamoDbDouble(object):

    def __init__(self):
        self._users = [{'email': 'bob@bob.bob'}]
        self.invoked_put_item = None


    def Table(self, table_name):
        return self


    def get_item(self, Key):
        email = Key.get('email')
        for user in self._users:
            if user.get('email') == email:
                return {'Item': user}
        return {}


    def put_item(self, Item):
        self.invoked_put_item = Item