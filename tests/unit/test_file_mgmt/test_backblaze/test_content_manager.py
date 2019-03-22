from collections import namedtuple
import hashlib
import unittest

import urllib

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
        self.user.content_credentials = self.credentials


    def test_invokes_authorizer(self):
        # Skip for this base class since there is no operation
        if self.__class__ is not TestContentManagerBase:
            self.assertEqual(self.authorizer.invoked_credentials, self.credentials)




class TestGenerateCredentials(TestContentManagerBase):

    def setUp(self):
        super(TestGenerateCredentials, self).setUp()
        self.content_manager.generate_credentials(self.user)


    def test_invokes_authorizer(self):
        self.assertIs(self.authorizer.invoked_user, self.user)




class TestRevokeCredentials(TestContentManagerBase):

    def test_invokes_authorizer(self):
        application_key_id = self.user.content_credentials.split(':')[0]
        self.content_manager.revoke_credentials(self.user)
        self.assertEqual(self.authorizer.invoked_application_key_id, application_key_id)



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

        expected_headers = {'Authorization': 'api_token'}
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

        expected_headers = {'Authorization': 'api_token'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)

        expected_params = {'fileId': self.content_id}
        self.assertEqual(self.requests.invoked_get_params, expected_params)


    def test_calls_delete_api(self):
        expected_url = f'https://api.example.com/{content_manager._DELETE_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_post_url, expected_url)

        expected_headers = {'Authorization': 'api_token'}
        self.assertEqual(self.requests.invoked_post_headers, expected_headers)

        expected_json = {'fileId': self.content_id, 'fileName': 'bobfile1.png'}
        self.assertEqual(self.requests.invoked_post_json, expected_json)



class TestUploadContent(TestContentManagerBase):

    def setUp(self):
        requests = common.RequestsDouble(None, UploadFileResponseDouble)
        super(TestUploadContent, self).setUp(requests)
        self.raw_file = FileDouble()
        self.content_id = self.content_manager.upload_content(self.raw_file, self.user)


    def test_gets_upload_authorization_from_api_authorization(self):
        self.assertEqual(self.authorizer.invoked_authorization.token, 'api_token')


    def test_invokes_upload_file_api(self):
        expected_url = 'https://some.long.upload.url'
        self.assertEqual(self.requests.invoked_post_url, expected_url)

        encoded_filename = urllib.parse.quote_plus(self.raw_file.filename)
        expected_headers = {
            'Authorization': 'upload_token',
            'X-Bz-File-Name': f'{self.user.username}/{encoded_filename}',
            'Content-Type': self.raw_file.mimetype,
            'Content-Length': str(len(self.raw_file.content)),
            'X-Bz-Content-Sha1': hashlib.sha1(self.raw_file.content).hexdigest(),

        }
        self.assertEqual(self.requests.invoked_post_headers, expected_headers)

        expected_data = self.raw_file.content
        self.assertEqual(self.requests.invoked_post_data, expected_data)


    def test_raises_exception_if_file_upload_failed(self):
        self.requests.post_status_code = '<anything not 200>'
        with self.assertRaises(exceptions.ContentUploadFailedError):
            self.content_manager.upload_content(self.raw_file, self.user)


    def test_returns_content_id_if_upload_succeeds(self):
        self.assertEqual(self.content_id, 'a-new-content-id')




class DownloadFileResponseDouble(common.ResponseDouble):

    def __init__(self, status_code):
        super(DownloadFileResponseDouble, self).__init__(status_code)
        self.content = b'some file content'



class FileInfoResponseDouble(common.ResponseDouble):

    def json(self):
        return {'fileName': 'bobfile1.png'}



class UploadFileResponseDouble(common.ResponseDouble):

    def json(self):
        return {'fileId': 'a-new-content-id'}



class FileDouble(object):

    def __init__(self):
        self.filename = 'index with spaces.html'
        self.mimetype = 'text/html'
        self.content = b'uploaded file bytes'


    def read(self):
        return self.content


class AuthorizerDouble(object):

    def __init__(self):
        self.invoked_credentials = None
        self.invoked_user = None
        self.invoked_authorization = None
        self.invoked_application_key_id = None


    def create_user_credentials(self, user):
        self.invoked_user = user


    def delete_user_credentials(self, application_key_id):
        self.invoked_application_key_id = application_key_id


    def authorize_api(self, credentials):
        self.invoked_credentials = credentials
        return Authorization('https://api.example.com', 'https://f002.example.com', 'api_token')


    def authorize_upload(self, authorization):
        self.invoked_authorization = authorization
        return UploadAuthorization('https://some.long.upload.url', 'upload_token')




Authorization = namedtuple('Authorization', ['api_url', 'download_url', 'token'])
UploadAuthorization = namedtuple('UploadAuthorization', ['upload_url', 'token'])


class UserDouble(object):

    def __init__(self, username):
        self.username = username
        self.content_credentials = None