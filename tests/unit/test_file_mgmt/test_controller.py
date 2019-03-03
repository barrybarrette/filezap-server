from collections import namedtuple
import unittest

import src.file_mgmt.controller as controller


class TestFileMgmtControllerBase(unittest.TestCase):

    def setUp(self):
        self.content_id = 'some_id'
        self.credentials = 'my:creds'
        self.user = UserDouble('bob', self.credentials)
        self.data_store = DataStoreDouble()
        self.content_manager = ContentManagerDouble()
        self.controller = controller.FileMgmtController(self.data_store, self.content_manager)




class TestGetFiles(TestFileMgmtControllerBase):

    def setUp(self):
        super(TestGetFiles, self).setUp()
        self.files = self.controller.get_files('steve')


    def test_invokes_data_store(self):
        self.assertEqual(self.data_store.invoked_username, 'steve')


    def test_returns_empty_list_if_user_has_no_files(self):
        self.assertEqual(self.files, [])


    def test_returns_files_for_user(self):
        self.data_store.files = ['file1', 'file2']
        files = self.controller.get_files('steve')
        self.assertEqual(files, ['file1', 'file2'])




class TestGetFile(TestFileMgmtControllerBase):

    def setUp(self):
        super(TestGetFile, self).setUp()
        self.file = self.controller.get_file(self.content_id, self.user)


    def test_invokes_data_store(self):
        self.assertEqual(self.data_store.invoked_content_id, self.content_id)
        self.assertEqual(self.data_store.invoked_username, self.user.username)


    def test_invokes_content_manager(self):
        self.assertEqual(self.content_manager.invoked_content_id, self.content_id)
        self.assertEqual(self.content_manager.invoked_credentials, self.user.content_credentials)


    def test_returns_file_with_content(self):
        self.assertEqual(self.file.content, b'these are file contents')




class TestDeleteFile(TestFileMgmtControllerBase):

    def setUp(self):
        super(TestDeleteFile, self).setUp()
        self.controller.delete_file(self.content_id, self.user)


    def test_invokes_data_store(self):
        self.assertEqual(self.data_store.invoked_content_id, self.content_id)
        self.assertEqual(self.data_store.invoked_username, self.user.username)


    def test_invokes_content_manager(self):
        self.assertEqual(self.content_manager.invoked_content_id, self.content_id)
        self.assertEqual(self.content_manager.invoked_credentials, self.credentials)


    def test_does_not_invoke_data_store_if_content_manager_raises_exception(self):
        self.data_store.invoked_content_id = None # Clear the invocation from setUp
        self.data_store.invoked_username = None   # Clear the invocation from setUp
        self.content_manager.should_raise = True
        with self.assertRaises(ExceptionDummy):
            self.controller.delete_file(self.content_id, self.user)
        self.assertIsNone(self.data_store.invoked_content_id)
        self.assertIsNone(self.data_store.invoked_username)




class TestSaveFile(TestFileMgmtControllerBase):

    def setUp(self):
        super(TestSaveFile, self).setUp()
        self.file = RawFileDouble()
        self.controller.save_file(self.file, self.user)


    def test_invokes_content_manager(self):
        self.assertIs(self.content_manager.invoked_file, self.file)
        self.assertIs(self.content_manager.invoked_user, self.user)


    def test_invokes_data_store(self):
        self.assertEqual(self.data_store.invoked_file.owner, self.user.username)
        self.assertEqual(self.data_store.invoked_file.filename, self.file.filename)
        self.assertEqual(self.data_store.invoked_file.content_id, 'a-new-content-id')


    def test_does_not_invoke_data_store_if_content_manager_raises_exception(self):
        self.data_store.invoked_file = None # Clear invocation from setUp
        self.content_manager.should_raise = True
        with self.assertRaises(ExceptionDummy):
            self.controller.save_file(self.file, self.user)
        self.assertIsNone(self.data_store.invoked_file)




UserDouble = namedtuple('UserDouble', ['username', 'content_credentials'])


class ContentManagerDouble(object):

    def __init__(self):
        self.invoked_content_id = None
        self.invoked_credentials = None
        self.invoked_file = None
        self.invoked_user = None
        self.should_raise = False


    def get_content(self, file_id, credentials):
        self.invoked_content_id = file_id
        self.invoked_credentials = credentials
        return b'these are file contents'


    def delete_content(self, content_id, credentials):
        self.invoked_content_id = content_id
        self.invoked_credentials = credentials
        if self.should_raise:
            raise ExceptionDummy()


    def upload_content(self, file, user):
        self.invoked_file = file
        self.invoked_user = user
        if self.should_raise:
            raise ExceptionDummy()
        return 'a-new-content-id'






class DataStoreDouble(object):

    def __init__(self):
        self.invoked_content_id = None
        self.invoked_username = None
        self.invoked_file = None
        self.files = []


    def get_files(self, username):
        self.invoked_username = username
        return self.files


    def get_file(self, content_id, username):
        self.invoked_content_id = content_id
        self.invoked_username = username
        return FileDummy()


    def remove_file(self, content_id, username):
        self.invoked_content_id = content_id
        self.invoked_username = username


    def add_file(self, file):
        self.invoked_file = file


class FileDummy(object):
    pass


class RawFileDouble(object):

    def __init__(self):
        self.filename = 'file.jpg'



class ExceptionDummy(Exception):
    pass