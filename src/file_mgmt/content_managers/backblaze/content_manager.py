from .authorization import Authorizer
from ..exceptions import ContentNotFoundError


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
        authorization = self._authorizer.authorize(credentials)
        response = self._download_content(authorization, content_id)
        return response.content


    def delete_content(self, content_id, credentials):
        """
        BackBlaze requires id AND filename to delete:
        https://www.backblaze.com/b2/docs/b2_delete_file_version.html

        Since FileZap doesn't know or care how a content manager stores
        a filename, we retrieve it from the BackBlaze API
        """
        authorization = self._authorizer.authorize(credentials)
        filename = self._get_filename(authorization, content_id)
        self._invoke_api_delete(authorization, content_id, filename)


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


    def _invoke_api_get(self, url, authorization, content_id):
        headers = {'Authorization': authorization.token}
        params = {'fileId': content_id}
        return self._requests.get(url, headers=headers, params=params)


    def _invoke_api_delete(self, authorization, content_id, filename):
        delete_url = f'{authorization.api_url}/{_DELETE_RELATIVE_URL}'
        headers = {'Authorization': authorization.token}
        json = {'fileId': content_id, 'fileName': filename}
        r = self._requests.post(delete_url, headers=headers, json=json)
        pass
