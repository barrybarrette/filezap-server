class UserDataStore(object):
    """
    Interface class for dynamodb users table
    """
    def __init__(self, config, dynamodb=None):
        """
        :param dynamodb: Only used for test mocking, do not pass in production code
        """
        if not dynamodb:
            import boto3
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self._table = dynamodb.Table(config.get('USER_DB_TABLE'))


    def add_user(self, user):
        if self._user_exists(user):
            raise DuplicateEmailError()
        self._table.put_item(Item=user.to_dict())


    def _user_exists(self, user):
        response = self._table.get_item(Key={'email': user.email})
        user_dict = response.get('Item')
        return True if user_dict else False




class DuplicateEmailError(Exception):
    pass