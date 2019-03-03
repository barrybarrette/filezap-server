from datetime import datetime
import unittest

import src.file_mgmt.model as model



class TestFile(unittest.TestCase):

    def setUp(self):
        self.owner = 'bob'
        self.filename = 'a_file.jpg'
        self.content_id = 'file_id'
        self.file = FileSpy(self.owner, self.filename, self.content_id)


    def test_uses_specified_attributes(self):
        self.assertEqual(self.file.owner, 'bob')
        self.assertEqual(self.file.filename, 'a_file.jpg')


    def test_sets_creation_time(self):
        self.assertEqual(self.file.created_at, FileSpy.now)


    def test_sets_content_to_none(self):
        self.assertIsNone(self.file.content)


    def test_to_dict(self):
        expected = {
            'owner': self.owner,
            'filename': self.filename,
            'created_at': FileSpy.now.strftime(model.DATE_FORMAT),
            'content_id': self.content_id
        }
        self.assertEqual(self.file.to_dict(), expected)


    def test_from_dict(self):
        created_at = datetime(2017, 9, 15)
        file_dict = {
            'owner': self.owner,
            'filename': self.filename,
            'created_at': created_at.strftime(model.DATE_FORMAT),
            'content_id': self.content_id
        }
        file = FileSpy.from_dict(file_dict)
        self.assertEqual(file.owner, self.owner)
        self.assertEqual(file.filename, self.filename)
        self.assertEqual(file.created_at, created_at)
        self.assertEqual(file.content_id, self.content_id)





class FileSpy(model.File):

    now = datetime.now()

    def _get_current_timestamp(self):
        return self.now