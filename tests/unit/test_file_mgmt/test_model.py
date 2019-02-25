from datetime import datetime
import unittest

import src.file_mgmt.model as model



class TestFile(unittest.TestCase):

    def setUp(self):
        self.owner = 'bob'
        self.native_file_object = NativeFileObjectDouble()
        self.file = FileSpy(self.owner, self.native_file_object)


    def test_uses_specified_attributes(self):
        self.assertEqual(self.file.owner, 'bob')
        self.assertIs(self.file.bytes, self.native_file_object.read())
        self.assertEqual(self.file.filename, 'a_file.jpg')


    def test_sets_creation_time(self):
        self.assertEqual(self.file.created_at, FileSpy.now)


    def test_to_dict(self):
        expected = {
            'owner': 'bob',
            'filename': 'a_file.jpg',
            'created_at': FileSpy.now.strftime(model.DATE_FORMAT),
            'bytes': self.native_file_object.read()
        }
        self.assertEqual(self.file.to_dict(), expected)


    def test_from_dict(self):
        created_at = datetime(2017, 9, 15)
        file_dict = {
            'owner': 'bob',
            'filename': 'a_file.jpg',
            'created_at': created_at.strftime(model.DATE_FORMAT),
            'bytes': self.native_file_object.read()
        }
        file = FileSpy.from_dict(file_dict)
        self.assertEqual(file.owner, 'bob')
        self.assertEqual(file.filename, 'a_file.jpg')
        self.assertEqual(file.created_at, created_at)
        self.assertEqual(file.bytes, self.native_file_object.read())


class NativeFileObjectDouble(object):

    def __init__(self):
        self.filename = 'a_file.jpg'


    def read(self):
        return b'this is a file and these are some bytes'


class FileSpy(model.File):

    now = datetime.now()

    def _get_current_timestamp(self):
        return self.now