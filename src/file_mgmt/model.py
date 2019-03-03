from datetime import datetime


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class File(object):

    def __init__(self, owner, filename, content_id, created_at=None):
        self.owner = owner
        self.filename = filename
        self.content_id = content_id
        self.created_at = created_at or self._get_current_timestamp()
        self.content = None


    def to_dict(self):
        return {
            'owner': self.owner,
            'filename': self.filename,
            'created_at': self.created_at.strftime(DATE_FORMAT),
            'content_id': self.content_id
        }


    @classmethod
    def from_dict(cls, file_dict):
        owner = file_dict.get('owner')
        filename = file_dict.get('filename')
        content_id = file_dict.get('content_id')
        created_at = datetime.strptime(file_dict.get('created_at'), DATE_FORMAT)
        return cls(owner, filename, content_id, created_at)


    def _get_current_timestamp(self):
        return datetime.now()
