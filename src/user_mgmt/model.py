class User(object):

    def __init__(self, email, password):
        self.email = email
        self.password_hash = password


    def to_dict(self):
        return {
            'email': self.email,
            'password_hash': self.password_hash
        }

    @classmethod
    def from_dict(cls, user_dict):
        return cls(user_dict.get('email'), user_dict.get('password_hash'))