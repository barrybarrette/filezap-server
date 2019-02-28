from collections import namedtuple
import unittest

import src.file_mgmt.controller as controller


class TestGetFile(unittest.TestCase):

    def setUp(self):
        self.file_id = 'some_id'
        self.user = UserDouble('bob', 'my creds')
        self.data_store = DataStoreDouble()
        self.content_manager = ContentManagerDouble()
        self.controller = controller.FileMgmtController(self.data_store, self.content_manager)
        self.file = self.controller.get_file(self.file_id, self.user)


    def test_raises_exception_if_file_owner_does_not_match(self):
        with self.assertRaises(controller.InvalidOwnerError):
            self.controller.get_file(self.file_id, UserDouble('<invalid user>', 'creds'))


    def test_invokes_data_store(self):
        self.assertEqual(self.data_store.invoked_file_id, self.file_id)
        self.assertEqual(self.data_store.invoked_username, self.user.username)


    def test_invokes_content_manager(self):
        self.assertEqual(self.content_manager.invoked_file_id, self.file_id)
        self.assertEqual(self.content_manager.invoked_credentials, self.user.content_credentials)


    def test_returns_file_with_content(self):
        self.assertEqual(self.file.content, b'these are file contents')



UserDouble = namedtuple('UserDouble', ['username', 'content_credentials'])


class ContentManagerDouble(object):

    def __init__(self):
        self.invoked_file_id = None
        self.invoked_credentials = None


    def get_content(self, file_id, credentials):
        self.invoked_file_id = file_id
        self.invoked_credentials = credentials
        return b'these are file contents'




class DataStoreDouble(object):

    def __init__(self):
        self.invoked_file_id = None
        self.invoked_username = None


    def get_file(self, file_id, username):
        self.invoked_file_id = file_id
        self.invoked_username = username
        return FileDouble(file_id)



class FileDouble(object):

    def __init__(self, file_id):
        self.id = file_id
        self.owner = 'bob'
        self.content = None
