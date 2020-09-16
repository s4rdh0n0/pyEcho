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
        'updatedate': None,
        'actived': False
    }

    def __init__(self, type="", host="", token=""):
        self.type = type
        super().__init__(host=host, token=token)

    def find(self, code=""):
        param = 'type={}&code={}'.format(self.type, code)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def get_master(self):
        param = 'type={}'.format(self.type)
        return  requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)
