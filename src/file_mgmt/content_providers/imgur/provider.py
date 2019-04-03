from io import BytesIO
import os


class ImgurContentProvider(object):
    """
    Takes an imgur gallery url and downloads each file in it

    Both client_class and requests_lib are used for testing only
    and should not be passed in production code
    """
    def __init__(self, client_class=None, requests_lib=None):
        client_id = os.environ.get('IMGUR_CLIENT_ID')
        client_secret = os.environ.get('IMGUR_CLIENT_SECRET')
        if not client_class:
            import imgurpython
            client_class = imgurpython.ImgurClient
        self._client = client_class(client_id, client_secret)
        self._requests = requests_lib
        if not self._requests:
            import requests
            self._requests = requests



    def get_files(self, url):
        album_id = url.split('/')[-1]
        images = self._client.get_album_images(album_id)
        for image in images:
            r = self._requests.get(image.link)
            file = BytesIO(r.content)
            file.filename = image.link.split('/')[-1]
            file.mimetype = r.headers.get('Content-Type')
            yield file
