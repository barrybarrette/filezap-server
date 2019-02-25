import base64

class User(object):

    def __init__(self, username, password_hash, salt):
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.is_authenticated = False


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
            'salt': base64.b64encode(self.salt).decode()
        }


    @classmethod
    def from_dict(cls, user_dict):
        return cls(user_dict.get('username'), user_dict.get('password_hash'), base64.b64decode(user_dict.get('salt')))



class UserManager(object):

    def __init__(self, user_data_store):
        self._users = {}
        self._user_data_store = user_data_store


    @property
    def user_count(self):
        return len(self._users)


    def get_user(self, username):
        return self._users.get(username)


    def add_user(self, user):
        self._do_add_user(user)
        self._user_data_store.add_user(user)


    def load_users(self):
        [self._do_add_user(user) for user in self._user_data_store.get_all_users()]


    def _do_add_user(self, user):
        if user.username in self._users:
            raise DuplicateUserError()
        self._users[user.username] = user



class DuplicateUserError(Exception):
    pass