from .model import File
import src.file_mgmt.content_providers as content_providers



class FileMgmtController(object):

    def __init__(self, data_store, content_manager):
        self._data_store = data_store
        self._content_manager = content_manager


    def get_files(self, username):
        return self._data_store.get_files(username)


    def get_file(self, content_id, user):
        file = self._data_store.get_file(content_id, user.username)
        file.content = self._content_manager.get_content(content_id, user.content_credentials)
        return file


    def delete_file(self, content_id, user):
        self._content_manager.delete_content(content_id, user.content_credentials)
        self._data_store.remove_file(content_id, user.username)


    def save_file(self, raw_file, user):
        content_id = self._content_manager.upload_content(raw_file, user)
        file = File(user.username, raw_file.filename, content_id)
        self._data_store.add_file(file)


    def save_file_from(self, content_url, user):
        content_provider = self._get_content_provider(content_url)
        for file in content_provider.get_files(content_url):
            self.save_file(file, user)


    def _get_content_provider(self, content_url):
        content_provider = None
        if content_url.startswith('https://imgur.com'):
            content_provider = self._get_imgur_provider()
        if not content_provider: raise URLNotSupportedError(content_url)
        return content_provider


    def _get_imgur_provider(self):
        return content_providers.ImgurContentProvider()


class URLNotSupportedError(Exception):
    pass
