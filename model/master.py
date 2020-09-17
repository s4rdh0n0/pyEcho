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

    def get_master(self):
        param = 'type={}'.format(self.type)
        return  requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, code=""):
        param = 'type={}&code={}'.format(self.type, code)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)


    def add(self, master={}):
        djson = {'master': master}
        return requests.post('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def update(self, code="", master={}):
        djson = {'type': self.type,
                 'code': code,
                 'master': master}
        return requests.put('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def delete(self, code=""):
        djson = {'type': self.type,
                 'code': code}
        return requests.delete('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)
