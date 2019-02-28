from .authorization import Authorizer

_DOWNLOAD_RELATIVE_URL = 'b2api/v2/b2_download_file_by_id'


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


    def get_content(self, file_id, credentials):
        authorization = self._authorizer.authorize(credentials)
        response = self._query_api(authorization, file_id)
        return response.content


    def _query_api(self, authorization, file_id):
        download_url = f'{authorization.download_url}/{_DOWNLOAD_RELATIVE_URL}'
        headers = {'Authorization': authorization.token}
        params = {'fileId': file_id}
        response = self._requests.get(download_url, headers=headers, params=params)
        return response
