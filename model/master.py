import requests

# Model
from model.base import BaseModel


class MasterModel(BaseModel):

    root = 'offices/master'

    schema = {
        '_id': None,
        'type': None,
        'code': None,
        'description': None,
        'createdate': None,
        'usercreate': None,
        'updatedate': None,
        'userupdate': None,
        'actived': False
    }

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)
