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
