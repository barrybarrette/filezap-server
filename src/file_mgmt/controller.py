class FileMgmtController(object):

    def __init__(self, data_store, content_manager):
        self._data_store = data_store
        self._content_manager = content_manager


    def get_file(self, file_id, user):
        file = self._get_file(file_id, user.username)
        file.content = self._content_manager.get_content(file_id, user.content_credentials)
        return file


    def _get_file(self, file_id, username):
        file = self._data_store.get_file(file_id, username)
        if file.owner != username: raise InvalidOwnerError()
        return file




class InvalidOwnerError(Exception):
    pass
