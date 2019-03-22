import base64



class User(object):
    def __init__(self, username, password_hash, salt, content_credentials=None, revocation=None):
        self.is_authenticated = False
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.content_credentials = content_credentials


    @property
    def is_active(self):
        return True


    @property
    def is_anonymous(self):
        return False


    def get_id(self):
        return self.username


    def to_dict(self):
        return {
            'username': self.username,
            'password_hash': self.password_hash,
            'salt': base64.b64encode(self.salt).decode(),
            'content_credentials': self.content_credentials
        }


    @classmethod
    def from_dict(cls, user_dict):
        user = cls(user_dict.get('username'),
                   user_dict.get('password_hash'),
                   base64.b64decode(user_dict.get('salt')),
                   user_dict.get('content_credentials'))
        return user



class UserManager(object):

    def __init__(self, user_data_store, file_data_store):
        self._users = {}
        self._user_data_store = user_data_store
        self._file_data_store = file_data_store


    @property
    def user_count(self):
        return len(self._users)


    def get_user(self, username):
        user = self._users.get(username)
        if not user:
            user = self._get_user_from_data_store(username)
        return user


    def add_user(self, user, content_manager):
        self._do_add_user(user)
        content_manager.generate_credentials(user)
        self._user_data_store.add_user(user)


    def delete_user(self, user, content_manager):
        self._delete_user_files(user, content_manager)
        content_manager.revoke_credentials(user)
        self._user_data_store.delete_user(user.username)
        self._users.pop(user.username)


    def _get_user_from_data_store(self, username):
        user = self._user_data_store.get_user(username)
        if user:
            self._users[username] = user
        return user


    def _do_add_user(self, user):
        if user.username in self._users:
            raise DuplicateUserError()
        self._users[user.username] = user


    def _delete_user_files(self, user, content_manager):
        for file in self._file_data_store.get_files(user.username):
            content_manager.delete_content(file.content_id, user.content_credentials)
            self._file_data_store.remove_file(file.content_id, user.username)


class DuplicateUserError(Exception):
    pass
