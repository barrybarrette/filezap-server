from ..exceptions import ContentManagerAuthorizationError

class BackBlazeAuthorizationError(ContentManagerAuthorizationError):

    def __init__(self, auth_string):
        self.auth_string = auth_string


    def __str__(self):
        return f'Invalid authentication string: {self.auth_string}'