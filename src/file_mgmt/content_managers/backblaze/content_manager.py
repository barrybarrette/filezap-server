import hashlib
import urllib

from .authorization import Authorizer
from ..exceptions import ContentNotFoundError, ContentUploadFailedError


_API_PREFIX = 'b2api/v2'
_DELETE_RELATIVE_URL = f'{_API_PREFIX}/b2_delete_file_version'
_DOWNLOAD_RELATIVE_URL = f'{_API_PREFIX}/b2_download_file_by_id'
_FILE_INFO_RELATIVE_URL = f'{_API_PREFIX}/b2_get_file_info'


class ContentManager(object):
    """
    """
    def __init__(self, authorizer=None, requests_lib=None):
        if not authorizer:
            authorizer = Authorizer()
        self._authorizer = authorizer
        if not requests_lib:
            import requests
            requests_lib = requests
        self._requests = requests_lib


    def generate_credentials(self, user):
        user.content_credentials = self._authorizer.create_user_credentials(user.username)


    def get_content(self, content_id, credentials):
        authorization = self._authorizer.authorize_api(credentials)
        response = self._download_content(authorization, content_id)
        return response.content


    def delete_content(self, content_id, credentials):
        """
        BackBlaze requires id AND filename to delete:
        https://www.backblaze.com/b2/docs/b2_delete_file_version.html

        Since FileZap doesn't know or care how a content manager stores
        a filename, we retrieve it from the BackBlaze API
        """
        authorization = self._authorizer.authorize_api(credentials)
        filename = self._get_filename(authorization, content_id)
        self._invoke_api_delete(authorization, content_id, filename)


    def upload_content(self, file, user):
        api_authorization = self._authorizer.authorize_api(user.content_credentials)
        upload_authorization = self._authorizer.authorize_upload(api_authorization)
        content_id = self._upload_file(upload_authorization, file, user.username)
        return content_id


    def _download_content(self, authorization, content_id):
        download_url = f'{authorization.download_url}/{_DOWNLOAD_RELATIVE_URL}'
        response = self._invoke_api_get(download_url, authorization, content_id)
        if response.status_code == 404:
            raise ContentNotFoundError()
        return response


    def _get_filename(self, authorization, content_id):
        file_info_url = f'{authorization.api_url}/{_FILE_INFO_RELATIVE_URL}'
        response = self._invoke_api_get(file_info_url, authorization, content_id)
        return response.json().get('fileName')


    def _upload_file(self, authorization, file, username):
        response = self._invoke_api_post(authorization, file, username)
        if response.status_code != 200:
            raise ContentUploadFailedError()
        return response.json().get('fileId')


    def _invoke_api_get(self, url, authorization, content_id):
        headers = {'Authorization': authorization.token}
        params = {'fileId': content_id}
        return self._requests.get(url, headers=headers, params=params)


    def _invoke_api_delete(self, authorization, content_id, filename):
        delete_url = f'{authorization.api_url}/{_DELETE_RELATIVE_URL}'
        headers = {'Authorization': authorization.token}
        json = {'fileId': content_id, 'fileName': filename}
        self._requests.post(delete_url, headers=headers, json=json)


    def _invoke_api_post(self, authorization, file, username):
        file_content = file.read()
        encoded_filename = urllib.parse.quote_plus(file.filename)
        headers = {
            'Authorization': authorization.token,
            'X-Bz-File-Name': f'{username}/{encoded_filename}',
            'Content-Type': file.mimetype,
            'Content-Length': str(len(file_content)),
            'X-Bz-Content-Sha1': hashlib.sha1(file_content).hexdigest()
        }
        return self._requests.post(authorization.upload_url, headers=headers, data=file_content)
