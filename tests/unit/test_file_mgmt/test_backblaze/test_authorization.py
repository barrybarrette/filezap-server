import base64
import os
import unittest

import src.file_mgmt.content_managers.backblaze.authorization as authorization
import src.file_mgmt.content_managers.backblaze.exceptions as exceptions
import tests.unit.test_file_mgmt.test_backblaze.common as common




class TestAuthorizeApi(unittest.TestCase):

    def setUp(self):
        self.requests = common.RequestsDouble(AuthorizeApiResponseDouble)
        self.authorizer = authorization.Authorizer(self.requests)
        self.credentials = 'app_id:secret_key'
        self.authorize_response = self.authorizer.authorize_api(self.credentials)


    def test_request_invokes_authorize_api(self):
        expected_url = authorization._AUTH_URL
        self.assertEqual(self.requests.invoked_get_url, expected_url)

        expected_headers = {'Authorization': f'Basic {as_base_64("app_id:secret_key")}'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)


    def test_raises_exception_if_bad_status_code_received(self):
        self.requests.get_status_code = "<anything that isn't 200>"
        with self.assertRaises(exceptions.ContentManagerAuthorizationError):
            self.authorizer.authorize_api(self.credentials)


    def test_returns_response_data_on_success(self):
        self.assertEqual(self.authorize_response.download_url, 'https://f002.example.com')
        self.assertEqual(self.authorize_response.token, 'a-token')
        self.assertEqual(self.authorize_response.api_url, 'https://api002.example.com')



class TestAuthorizeUpload(unittest.TestCase):

    def setUp(self):
        self.requests = common.RequestsDouble(AuthorizeUploadResponseDouble)
        self.authorizer = authorization.Authorizer(self.requests)
        self.credentials = 'app_id:secret_key'
        self.api_authorization = self.authorizer.authorize_api(self.credentials)
        self.requests.invoked_get_url = None
        self.requests.invoked_get_headers = None
        os.environ[authorization._ENV_BUCKET_ID] = 'bucket_id'
        self.authorize_response = self.authorizer.authorize_upload(self.api_authorization)


    def tearDown(self):
        os.environ.pop(authorization._ENV_BUCKET_ID)


    def test_request_invokes_authorize_upload_api(self):
        expected_url = f'{self.api_authorization.api_url}/{authorization._UPLOAD_AUTH_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_get_url, expected_url)

        expected_headers = {'Authorization': self.api_authorization.token}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)

        expected_params = {'bucketId': 'bucket_id'}
        self.assertEqual(self.requests.invoked_get_params, expected_params)


    def test_returns_upload_authorization(self):
        self.assertEqual(self.authorize_response.upload_url, 'https://upload.example.com')
        self.assertEqual(self.authorize_response.token, 'an-upload-token')




class TestCreateUserCredentials(unittest.TestCase):

    def setUp(self):
        self.setUpEnv()
        self.requests = common.RequestsDouble(AuthorizeApiResponseDouble, PostResponseDouble)
        self.authorizer = authorization.Authorizer(self.requests)
        self.credentials = self.authorizer.create_user_credentials('bob')


    def setUpEnv(self):
        os.environ[authorization._ENV_ACCOUNT_ID] = 'account_id'
        os.environ[authorization._ENV_BUCKET_ID] = 'bucket_id'
        os.environ[authorization._ENV_MASTER_APP_ID] = 'master app id'
        os.environ[authorization._ENV_MASTER_SECRET_KEY] = 'master secret key'
        os.environ['FILEZAP_ENV'] = 'PRODUCTION'


    def tearDown(self):
        os.environ.pop(authorization._ENV_ACCOUNT_ID)
        os.environ.pop(authorization._ENV_BUCKET_ID)
        os.environ.pop(authorization._ENV_MASTER_APP_ID)
        os.environ.pop(authorization._ENV_MASTER_SECRET_KEY)
        os.environ.pop('FILEZAP_ENV')



    def test_raises_exception_if_master_authorization_fails(self):
        self.requests.get_status_code = '<anything not 200>'
        with self.assertRaises(exceptions.BackBlazeAuthorizationError):
            self.authorizer.create_user_credentials('bob')


    def test_authorizes_with_master_credentials(self):
        expected_auth_header = {'Authorization': f'Basic {as_base_64("master app id:master secret key")}'}
        self.assertEqual(self.requests.invoked_get_url, authorization._AUTH_URL)
        self.assertEqual(self.requests.invoked_get_headers, expected_auth_header)


    def test_request_invokes_correct_url(self):
        expected_url = f'https://api002.example.com/{authorization._CREATE_KEY_RELATIVE_URL}'
        self.assertEqual(self.requests.invoked_post_url, expected_url)


    def test_request_sends_authorization_header(self):
        expected_auth_header = {'Authorization': 'a-token'}
        self.assertEqual(self.requests.invoked_post_headers, expected_auth_header)


    def test_request_sends_required_json_data(self):
        expected_json = {
            "accountId": "account_id",
            "capabilities": ["readFiles", "writeFiles", "deleteFiles"],
            "keyName": "filezap-bob",
            "bucketId": "bucket_id",
            "namePrefix": "bob/"
        }
        self.assertEqual(self.requests.invoked_post_json, expected_json)


    def test_specifies_dev_in_key_name_if_non_prod_environment(self):
        os.environ['FILEZAP_ENV'] = 'NON PROD'
        self.authorizer.create_user_credentials('bob')
        expected_json = {
            "accountId": "account_id",
            "capabilities": ["readFiles", "writeFiles", "deleteFiles"],
            "keyName": "filezap-dev-bob",
            "bucketId": "bucket_id",
            "namePrefix": "bob/"
        }
        self.assertEqual(self.requests.invoked_post_json, expected_json)


    def test_raises_exception_if_user_authentication_fails(self):
        self.requests.post_status_code = '<anything not 200>'
        with self.assertRaises(exceptions.BackBlazeAuthorizationError):
            self.authorizer.create_user_credentials('bob')


    def test_returns_credentials(self):
        self.assertEqual(self.credentials, 'app id:secret key')


# Helper
def as_base_64(auth_string):
    return base64.b64encode(auth_string.encode()).decode()




class AuthorizeApiResponseDouble(common.ResponseDouble):

    def json(self):
        return {
            "absoluteMinimumPartSize": 5000000,
            "accountId": "some_id",
            "allowed": {
                "bucketId": None,
                "bucketName": None,
                "capabilities": [
                    "writeKeys"
                ],
                "namePrefix": None
            },
            "apiUrl": "https://api002.example.com",
            "authorizationToken": "a-token",
            "downloadUrl": "https://f002.example.com",
            "recommendedPartSize": 100000000
        }




class AuthorizeUploadResponseDouble(common.ResponseDouble):

    def json(self):
        return {
            'uploadUrl': 'https://upload.example.com',
            'authorizationToken': 'an-upload-token'
        }



class PostResponseDouble(common.ResponseDouble):

    def json(self):
        return {
            "accountId": "account_id",
            "applicationKey": "secret key",
            "applicationKeyId": "app id",
            "bucketId": "bucket_id",
            "capabilities": [
                "readFiles",
                "writeFiles"
            ],
            "expirationTimestamp": 60000000000,
            "keyName": "filezap-dev-bob",
            "namePrefix": "bob/"
        }
