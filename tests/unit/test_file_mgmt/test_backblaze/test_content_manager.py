from collections import namedtuple
import unittest

import tests.unit.test_file_mgmt.test_backblaze.common as common
import src.file_mgmt.content_managers.backblaze.content_manager as content_manager
import src.file_mgmt.content_managers.exceptions as exceptions




class TestContentManagerBase(unittest.TestCase):

    def setUp(self, requests=None):
        self.requests = requests or common.RequestsDouble()
        self.authorizer = AuthorizerDouble()
        self.content_manager = content_manager.ContentManager(self.authorizer, self.requests)
        self.user = UserDouble('bob')
        self.content_id = 'a_content_id'
        self.credentials = 'my:creds'



class TestGenerateCredentials(TestContentManagerBase):

    def setUp(self):
        super(TestGenerateCredentials, self).setUp()
        self.content_manager.generate_credentials(self.user)


    def test_invokes_authorizer(self):
        self.assertEqual(self.authorizer.invoked_username, 'bob')


    def test_sets_user_content_credentials(self):
        self.assertEqual(self.user.content_credentials, 'bobs credentials')



class TestGetContent(TestContentManagerBase):

    def setUp(self):
        requests = common.RequestsDouble(DownloadFileResponseDouble)
        super(TestGetContent, self).setUp(requests)
        self.file_content = self.content_manager.get_content(self.content_id, self.credentials)


    def test_invokes_authorizer(self):
        self.assertEqual(self.authorizer.invoked_credentials, self.credentials)


    def test_calls_download_api(self):
        expected_url = f'https://f002.example.com/{content_manager._DOWNLOAD_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_get_url, expected_url)

        expected_headers = {'Authorization': 'a_token'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)

        expected_params = {'fileId': self.content_id}
        self.assertEqual(self.requests.invoked_get_params, expected_params)


    def test_raises_exception_if_file_not_found(self):
        self.requests.get_status_code = 404
        with self.assertRaises(exceptions.ContentNotFoundError):
            self.content_manager.get_content(self.content_id, self.credentials)


    def test_returns_file_content(self):
        self.assertEqual(self.file_content, b'some file content')



class TestDeleteContent(TestContentManagerBase):

    def setUp(self):
        requests = common.RequestsDouble(FileInfoResponseDouble)
        super(TestDeleteContent, self).setUp(requests)
        self.content_manager.delete_content(self.content_id, self.credentials)


    def test_invokes_authorizer(self):
        self.assertEqual(self.authorizer.invoked_credentials, self.credentials)


    def test_calls_get_file_api(self):
        expected_url = f'https://api.example.com/{content_manager._FILE_INFO_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_get_url, expected_url)

        expected_headers = {'Authorization': 'a_token'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)

        expected_params = {'fileId': self.content_id}
        self.assertEqual(self.requests.invoked_get_params, expected_params)


    def test_calls_delete_api(self):
        expected_url = f'https://api.example.com/{content_manager._DELETE_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_post_url, expected_url)

        expected_headers = {'Authorization': 'a_token'}
        self.assertEqual(self.requests.invoked_post_headers, expected_headers)

        expected_json = {'fileId': self.content_id, 'fileName': 'bobfile1.png'}
        self.assertEqual(self.requests.invoked_post_json, expected_json)





class DownloadFileResponseDouble(common.ResponseDouble):

    def __init__(self, status_code):
        super(DownloadFileResponseDouble, self).__init__(status_code)
        self.content = b'some file content'



class FileInfoResponseDouble(common.ResponseDouble):

    def __init__(self, status_code):
        super(FileInfoResponseDouble, self).__init__(status_code)


    def json(self):
        return {'fileName': 'bobfile1.png'}



class AuthorizerDouble(object):

    def __init__(self):
        self.invoked_credentials = None
        self.invoked_username = None


    def create_user_credentials(self, username):
        self.invoked_username = username
        return 'bobs credentials'


    def authorize(self, credentials):
        self.invoked_credentials = credentials
        return Authorization('https://api.example.com', 'https://f002.example.com', 'a_token')


Authorization = namedtuple('Authorization', ['api_url', 'download_url', 'token'])



class UserDouble(object):

    def __init__(self, username):
        self.username = username
        self.content_credentials = None