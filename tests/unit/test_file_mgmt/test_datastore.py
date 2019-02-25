import unittest

from boto3.dynamodb.conditions import Attr

import src.file_mgmt.datastore as datastore
import src.file_mgmt.model as model



class TestFileDataStore(unittest.TestCase):

    def setUp(self):
        self.dynamodb = DynamoDbDouble()
        config = {'FILE_DB_TABLE': 'the_file_table'}
        self.data_store = datastore.FileDataStore(config, self.dynamodb)


    def test_uses_configured_table_name(self):
        self.assertEqual(self.dynamodb.invoked_table, 'the_file_table')


    def test_can_add_file_to_dynamo_db(self):
        file = model.File('bob', FileDouble())
        self.data_store.add_file(file)
        self.assertEqual(self.dynamodb.invoked_put_item, file.to_dict())


    def test_can_get_all_files_for_owner(self):
        files = self.data_store.get_files('bob')
        self.assertEqual(self.dynamodb.invoked_scan_filter, Attr('owner').eq('bob'))
        self.assertEqual(len(files), 2)
        for file in files:
            self.assertIsInstance(file, model.File)




class DynamoDbDouble(object):

    def __init__(self):
        self._files = [
            model.File('bob', FileDouble()).to_dict(),
            model.File('bob', FileDouble()).to_dict()
        ]
        self.invoked_put_item = None
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



class FileDouble(object):

    def __init__(self):
        self.filename = 'a_file.jpg'


    def read(self):
        return b'file bytes'