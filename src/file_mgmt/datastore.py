from boto3.dynamodb.conditions import Attr

import src.file_mgmt.model as model



class FileDataStore(object):

    def __init__(self, config, dynamodb=None):
        if not dynamodb:
            import boto3
            dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self._table = dynamodb.Table(config.get('FILE_DB_TABLE'))


    def add_file(self, file):
        self._table.put_item(Item=file.to_dict())


    def get_files(self, owner):
        response = self._table.scan(FilterExpression=Attr('owner').eq(owner))
        return [model.File.from_dict(file_dict) for file_dict in response.get('Items')]