from io import BytesIO
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class File(object):

    def __init__(self, owner, file_object, created_at=None):
        self.owner = owner
        self.bytes = file_object.read()
        self.filename = file_object.filename
        self.created_at = created_at or self._get_current_timestamp()


    def to_dict(self):
        return {
            'owner': self.owner,
            'filename': self.filename,
            'created_at': self.created_at.strftime(DATE_FORMAT),
            'bytes': self.bytes
        }


    @classmethod
    def from_dict(cls, file_dict):
        owner = file_dict.get('owner')
        file_object = _BytesWrapper(file_dict.get('bytes'), file_dict.get('filename'))
        created_at = datetime.strptime(file_dict.get('created_at'), DATE_FORMAT)
        return cls(owner, file_object, created_at)


    def _get_current_timestamp(self):
        return datetime.now()


class _BytesWrapper(BytesIO):

    def __init__(self, file_bytes, filename):
        super(_BytesWrapper, self).__init__(file_bytes)
        self.filename = filename