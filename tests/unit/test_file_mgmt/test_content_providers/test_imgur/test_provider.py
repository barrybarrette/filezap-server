import os
import unittest


import src.file_mgmt.content_providers as providers



class TestImgurContentProvider(unittest.TestCase):

    def setUp(self):
        os.environ['IMGUR_CLIENT_ID'] = 'a-client-id'
        os.environ['IMGUR_CLIENT_SECRET'] = 'a-client-secret'
        self.requests = RequestsDouble()
        self.provider = providers.ImgurContentProvider(ImgurClientDouble, self.requests)
        self.client = self.provider._client
        self.url = 'https://imgur.com/a/oUVDxci'
        self.files = list(self.provider.get_files(self.url))


    def tearDown(self):
        os.environ.pop('IMGUR_CLIENT_ID')
        os.environ.pop('IMGUR_CLIENT_SECRET')


    def test_gets_credentials_from_environment(self):
        self.assertEqual(self.client.client_id, 'a-client-id')
        self.assertEqual(self.client.client_secret, 'a-client-secret')


    def test_gets_download_links(self):
        self.assertEqual(self.client.invoked_album_id, 'oUVDxci')


    def test_downloads_each_file(self):
        self.assertEqual(self.requests.invoked_get_urls, ['url/to/file1.png', 'url/to/file2.jpg'])


    def test_returns_file_objects(self):
        file_1 = self.files[0]
        self.assertEqual(file_1.filename, 'file1.png')
        self.assertEqual(file_1.mimetype, 'image/png')
        self.assertEqual(file_1.read(), b'some file content')
        file_2 = self.files[1]
        self.assertEqual(file_2.filename, 'file2.jpg')
        self.assertEqual(file_2.mimetype, 'image/jpg')
        self.assertEqual(file_2.read(), b'some file content')



class ImgurClientDouble(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.invoked_album_id = None


    def get_album_images(self, album_id):
        self.invoked_album_id = album_id
        return [ImageDouble('url/to/file1.png'), ImageDouble('url/to/file2.jpg')]


class ImageDouble(object):

    def __init__(self, link):
        self.link = link


class RequestsDouble(object):

    def __init__(self):
        self.invoked_get_urls = []


    def get(self, url: str):
        self.invoked_get_urls.append(url)
        if url.endswith('.png'):
            return ResponseDouble('png')
        return ResponseDouble('jpg')


class ResponseDouble(object):

    def __init__(self, mime_type):
        self.content = b'some file content'
        self.headers = {'Content-Type': f'image/{mime_type}'}
