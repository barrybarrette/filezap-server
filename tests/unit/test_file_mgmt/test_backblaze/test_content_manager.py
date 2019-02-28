from collections import namedtuple
import unittest

import tests.unit.test_file_mgmt.test_backblaze.common as common
import src.file_mgmt.content_managers.backblaze.content_manager as content_manager



class TestGenerateCredentials(unittest.TestCase):

    def setUp(self):
        self.requests = common.RequestsDouble(ResponseDouble)
        self.authorizer = AuthorizerDouble()
        self.content_manager = content_manager.ContentManager(self.authorizer, self.requests)
        self.user = UserDouble('bob')
        self.content_manager.generate_credentials(self.user)


    def test_invokes_authorizer(self):
        self.assertEqual(self.authorizer.invoked_username, 'bob')


    def test_sets_user_content_credentials(self):
        self.assertEqual(self.user.content_credentials, 'bobs credentials')



class TestGetContent(unittest.TestCase):

    def setUp(self):
        self.requests = common.RequestsDouble(ResponseDouble)
        self.authorizer = AuthorizerDouble()
        self.content_manager = content_manager.ContentManager(self.authorizer, self.requests)
        self.file_id = 'a_file_id'
        self.credentials = 'my:creds'
        self.file_content = self.content_manager.get_content(self.file_id, self.credentials)


    def test_invokes_authorizer(self):
        self.assertEqual(self.authorizer.invoked_credentials, 'my:creds')


    def test_invokes_download_url(self):
        expected_url = f'https://f002.example.com/{content_manager._DOWNLOAD_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_get_url, expected_url)


    def test_sets_correct_authorization_headers(self):
        expected_headers = {'Authorization': 'a_token'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)


    def test_sets_correct_url_params(self):
        expected_params = {'fileId': self.file_id}
        self.assertEqual(self.requests.invoked_get_params, expected_params)


    def test_returns_file_content(self):
        self.assertEqual(self.file_content, b'some file content')



class ResponseDouble(common.ResponseDouble):

    def __init__(self, status_code):
        super(ResponseDouble, self).__init__(status_code)
        self.content = b'some file content'



class AuthorizerDouble(object):

    def __init__(self):
        self.invoked_credentials = None
        self.invoked_username = None


    def create_user_credentials(self, username):
        self.invoked_username = username
        return 'bobs credentials'


    def authorize(self, credentials):
        self.invoked_credentials = credentials
        return Authorization('https://f002.example.com', 'a_token')


Authorization = namedtuple('Authorization', ['download_url', 'token'])



class UserDouble(object):

    def __init__(self, username):
        self.username = username
        self.content_credentials = None