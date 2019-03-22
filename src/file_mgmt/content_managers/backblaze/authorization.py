import base64
from collections import namedtuple
import os

import src.config_manager as config_manager
from .exceptions import BackBlazeAuthorizationError



_ENV_ACCOUNT_ID = 'BACKBLAZE_ACCOUNT_ID'
_ENV_BUCKET_ID = 'BACKBLAZE_BUCKET_ID'
_ENV_MASTER_APP_ID = 'BACKBLAZE_MASTER_APP_ID'
_ENV_MASTER_SECRET_KEY = 'BACKBLAZE_MASTER_SECRET_KEY'
_AUTH_DURATION_SECONDS = 30


_AUTH_URL = 'https://api.backblazeb2.com/b2api/v2/b2_authorize_account'
_CREATE_KEY_RELATIVE_URL = 'b2api/v2/b2_create_key'
_DELETE_KEY_RELATIVE_URL = 'b2api/v2/b2_delete_key'
_UPLOAD_AUTH_RELATIVE_URL = 'b2api/v2/b2_get_upload_url'




class Authorizer(object):
    """
    Authorization client for BackBlaze. Requests lib is used for testing only and
    should not be passed in production code.
    """
    def __init__(self, requests_lib=None):
        if not requests_lib:
            import requests
            requests_lib = requests
        self._requests = requests_lib


    def authorize_api(self, credentials):
        self._query_auth_api(credentials)
        if self._api_response.status_code != 200:
            raise BackBlazeAuthorizationError(credentials)
        return self._make_authorize_response(self._api_response.json())


    def authorize_upload(self, api_authorization):
        authorize_upload_url = f'{api_authorization.api_url}/{_UPLOAD_AUTH_RELATIVE_URL}'
        headers = {'Authorization': api_authorization.token}
        params = {'bucketId': os.environ.get(_ENV_BUCKET_ID)}
        response = self._requests.get(authorize_upload_url, headers=headers, params=params)
        response_json = response.json()
        return _UploadAuthorization(response_json.get('uploadUrl'), response_json.get('authorizationToken'))


    def create_user_credentials(self, user):
        authorization = self._get_master_authorization()
        self._generate_application_key(authorization, user.username)
        response_data = self._api_response.json()
        user.content_credentials = f'{response_data.get("applicationKeyId")}:{response_data.get("applicationKey")}'



    def delete_user_credentials(self, application_key_id):
        authorization = self._get_master_authorization()
        self._delete_application_key(authorization, application_key_id)


    def _query_auth_api(self, credentials):
        self._build_auth_headers(credentials)
        self._api_response = self._requests.get(_AUTH_URL, headers=self._headers)


    def _make_authorize_response(self, response_data):
        download_url = response_data.get('downloadUrl')
        return _Authorization(response_data.get('apiUrl'),
                              download_url,
                              response_data.get('authorizationToken'))


    def _generate_application_key(self, authorization, username):
        create_key_url = f'{authorization.api_url}/{_CREATE_KEY_RELATIVE_URL}'
        key_name = f'filezap-{username}' if config_manager.is_production_environment() else f'filezap-dev-{username}'
        post_json = {
            'accountId': os.environ.get(_ENV_ACCOUNT_ID),
            'capabilities': ['readFiles', 'writeFiles', 'deleteFiles'],
            'keyName': key_name,
            'bucketId': os.environ.get(_ENV_BUCKET_ID),
            'namePrefix': f'{username}/'
        }
        self._api_response = self._requests.post(create_key_url, headers={'Authorization': authorization.token}, json=post_json)
        if self._api_response.status_code != 200:
            raise BackBlazeAuthorizationError(authorization.token)


    def _build_auth_headers(self, auth_string):
        auth_string_bytes = auth_string.encode()
        auth_string_as_base64 = base64.b64encode(auth_string_bytes).decode()
        self._headers = {'Authorization': f'Basic {auth_string_as_base64}'}


    def _get_master_authorization(self):
        master_credentials = f'{os.environ.get(_ENV_MASTER_APP_ID)}:{os.environ.get(_ENV_MASTER_SECRET_KEY)}'
        return self.authorize_api(master_credentials)


    def _delete_application_key(self, authorization, application_key_id):
        delete_key_url = f'{authorization.api_url}/{_DELETE_KEY_RELATIVE_URL}'
        post_json = {'applicationKeyId': application_key_id}
        self._requests.post(delete_key_url, headers={'Authorization': authorization.token}, json=post_json)



_Authorization = namedtuple('Authorization', ['api_url', 'download_url', 'token'])
_UploadAuthorization = namedtuple('UploadAuthorization', ['upload_url', 'token'])
