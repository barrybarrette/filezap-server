class ContentManagerAuthorizationError(Exception):
    """
    Content manager implementations should subclass this for authorization related errors
    """
    pass


class ContentNotFoundError(Exception):
    pass


class ContentUploadFailedError(Exception):
    pass
