class RequestsDouble(object):

    def __init__(self, get_response_class, post_response_class=None):
        self.get_status_code = 200
        self.post_status_code = 200
        self.invoked_get_url = None
        self.invoked_post_url = None
        self.invoked_get_headers = None
        self.invoked_post_headers = None
        self.invoked_get_params = None
        self.invoked_post_json = None
        self._get_response_class = get_response_class
        self._post_response_class = post_response_class


    def get(self, url, **kwargs):
        self.invoked_get_url = url
        self.invoked_get_headers = kwargs.get('headers')
        self.invoked_get_params = kwargs.get('params')
        return self._get_response_class(self.get_status_code)


    def post(self, url, **kwargs):
        self.invoked_post_url = url
        self.invoked_post_headers = kwargs.get('headers')
        self.invoked_post_json = kwargs.get('json')
        return self._post_response_class(self.post_status_code)


class ResponseDouble(object):

    def __init__(self, status_code):
        self.status_code = status_code