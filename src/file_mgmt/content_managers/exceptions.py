class ContentManagerAuthorizationError(Exception):
    """
    Content manager implementations should subclass this for authorization related errors
    """
    pass

#TODO: Implement raising ContentNotFoundError for b2
class ContentNotFoundError(Exception):
    pass
