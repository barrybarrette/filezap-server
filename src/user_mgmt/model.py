import base64

class User(object):

    def __init__(self, email, password_hash, salt):
        self.email = email
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
        return self.email


    def to_dict(self):
        return {
            'email': self.email,
            'password_hash': self.password_hash,
            'salt': base64.b64encode(self.salt).decode()
        }


    @classmethod
    def from_dict(cls, user_dict):
        return cls(user_dict.get('email'), user_dict.get('password_hash'), base64.b64decode(user_dict.get('salt')))



class UserManager(object):

    def __init__(self, user_data_store):
        self._users = {}
        self._user_data_store = user_data_store


    @property
    def user_count(self):
        return len(self._users)


    def get_user(self, email):
        return self._users.get(email)


    def add_user(self, user):
        self._do_add_user(user)
        self._user_data_store.add_user(user)


    def load_users(self):
        [self._do_add_user(user) for user in self._user_data_store.get_all_users()]


    def _do_add_user(self, user):
        if user.email in self._users:
            raise DuplicateUserError()
        self._users[user.email] = user



class DuplicateUserError(Exception):
    pass