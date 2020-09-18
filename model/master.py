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

    def __init__(self, host="", token=""):
        super().__init__(host=host, token=token)

    def get_master(self, type=""):
        param = 'type={}'.format(type)
        return  requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

    def count(self, type="", code=""):
        param = 'type={}&code={}'.format(type, code)
        return requests.get('{}/{}/count?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, type ="", code=""):
        param = 'type={}&code={}'.format(type, code)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def add(self, master={}):
        djson = {'master': master}
        return requests.post('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def update(self, type="", code="", master={}):
        djson = {'type': type,
                 'code': code,
                 'master': master}
        return requests.put('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def delete(self, type="", code=""):
        djson = {'type': type,
                 'code': code}
        return requests.delete('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)
