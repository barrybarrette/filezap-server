import base64
import os
import unittest

import src.file_mgmt.content_managers.backblaze.authorization as authorization
import src.file_mgmt.content_managers.backblaze.exceptions as exceptions
import tests.unit.test_file_mgmt.test_backblaze.common as common




class TestAuthorize(unittest.TestCase):

    def setUp(self):
        self.requests = common.RequestsDouble(GetResponseDouble)
        self.authorizer = authorization.Authorizer(self.requests)
        self.credentials = 'app_id:secret_key'
        self.authorize_response = self.authorizer.authorize(self.credentials)


    def test_request_invokes_correct_url(self):
        self.assertEqual(self.requests.invoked_get_url, authorization._AUTH_URL)


    def test_request_sends_authorization_header(self):
        expected_headers = {'Authorization': f'Basic {as_base_64("app_id:secret_key")}'}
        self.assertEqual(self.requests.invoked_get_headers, expected_headers)


    def test_raises_exception_if_bad_status_code_received(self):
        self.requests.get_status_code = "<anything that isn't 200>"
        with self.assertRaises(exceptions.ContentManagerAuthorizationError):
            self.authorizer.authorize(self.credentials)


    def test_returns_response_data_on_success(self):
        self.assertEqual(self.authorize_response.download_url, 'https://f002.example.com')
        self.assertEqual(self.authorize_response.token, 'a-token')
        self.assertEqual(self.authorize_response.api_url, 'https://api002.example.com')




class TestCreateUserCredentials(unittest.TestCase):

    def setUp(self):
        self.setUpEnv()
        self.requests = common.RequestsDouble(GetResponseDouble, PostResponseDouble)
        self.authorizer = authorization.Authorizer(self.requests)
        self.credentials = self.authorizer.create_user_credentials('bob')


    def setUpEnv(self):
        os.environ[authorization._ENV_ACCOUNT_ID] = 'account_id'
        os.environ[authorization._ENV_BUCKET_ID] = 'bucket_id'
        os.environ[authorization._ENV_MASTER_APP_ID] = 'master app id'
        os.environ[authorization._ENV_MASTER_SECRET_KEY] = 'master secret key'


    def tearDown(self):
        os.environ.pop(authorization._ENV_ACCOUNT_ID)
        os.environ.pop(authorization._ENV_MASTER_APP_ID)
        os.environ.pop(authorization._ENV_MASTER_SECRET_KEY)


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




class GetResponseDouble(common.ResponseDouble):

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
