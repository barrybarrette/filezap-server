import unittest

from boto3.dynamodb.conditions import Attr

import src.file_mgmt.datastore as datastore
import src.file_mgmt.model as model



class TestFileDataStoreBase(unittest.TestCase):

    def setUp(self):
        self.dynamodb = DynamoDbDouble()
        config = {'FILE_DB_TABLE': 'the_file_table'}
        self.data_store = datastore.FileDataStore(config, self.dynamodb)



class TestFileDataStore(TestFileDataStoreBase):

    def test_uses_configured_table_name(self):
        self.assertEqual(self.dynamodb.invoked_table, 'the_file_table')



class TestAddFile(TestFileDataStoreBase):

    def test_can_add_file_to_dynamo_db(self):
        file = model.File('bob', 'a_file.jpg', 'content_id')
        self.data_store.add_file(file)
        self.assertEqual(self.dynamodb.invoked_put_item, file.to_dict())



class TestRemoveFile(TestFileDataStoreBase):


    def test_deletes_file_from_dynamo_db(self):
        content_id = 'content_id_3'
        owner = 'alice'
        file = model.File(owner, 'a_file.jpg', content_id)
        self.data_store.add_file(file)
        self.data_store.remove_file(content_id, owner)
        self.assertEqual(self.dynamodb.invoked_delete_key, {'content_id': content_id, 'owner': owner})



class TestGetFile(TestFileDataStoreBase):

    def test_raises_exception_if_file_not_found(self):
        with self.assertRaises(datastore.FileNotFoundError):
            self.data_store.get_file('<invalid file id>', 'bob')


    def test_can_get_specific_file(self):
        content_id = 'content_id_2'
        file = self.data_store.get_file(content_id, 'bob')
        self.assertEqual(self.dynamodb.invoked_get_key, {'content_id': content_id, 'owner': 'bob'})
        self.assertEqual(file.content_id, content_id)



    def test_can_get_all_files_for_owner(self):
        files = self.data_store.get_files('bob')
        self.assertEqual(self.dynamodb.invoked_scan_filter, Attr('owner').eq('bob'))
        self.assertEqual(len(files), 2)
        for file in files:
            self.assertIsInstance(file, model.File)




class DynamoDbDouble(object):

    def __init__(self):
        self._files = [
            model.File('bob', 'a_file.jpg', 'content_id_1').to_dict(),
            model.File('bob', 'a_file.png', 'content_id_2').to_dict()
        ]
        self.invoked_put_item = None
        self.invoked_get_key = None
        self.invoked_delete_key = None
        self.invoked_table = None
        self.invoked_scan_filter = None


    def Table(self, table_name):
        self.invoked_table = table_name
        return self


    def put_item(self, Item):
        self.invoked_put_item = Item


    def scan(self, FilterExpression):
        self.invoked_scan_filter = FilterExpression
        return {'Items': self._files}


    def get_item(self, Key):
        self.invoked_get_key = Key
        specified_file_id = Key.get('content_id')
        if specified_file_id == '<invalid file id>':
            return {}
        return {'Item': model.File('bob', 'a_file.jpg', specified_file_id).to_dict()}


    def delete_item(self, Key):
        self.invoked_delete_key = Key