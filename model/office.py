import requests
import datetime

# Model
from model.base import BaseModel


class OfficeModel(BaseModel):

    root = 'offices'

    def __init__(self, host="", token=""):
        super().__init__(host=host, token=token)

    def schema(self):
        return requests.get('{}/{}/schema'.format(self.host, self.root), headers=self.header)

    def all(self):
        return requests.get('{}/{}'.format(self.host, self.root), headers=self.header)

    def kkpTolocal(self, officeid="", kkp={}, actived=False):
        result = self.schema().json()['result']
        result['_id'] = officeid
        result['code'] = kkp['code']
        result['officetypeid'] = kkp['officetypeid']
        result['parent'] = kkp['parent']
        result['nama'] = kkp['name']
        result['kota'] = kkp['city']
        result['alamat'] = kkp['address']
        result['phone'] = kkp['phone']
        result['email'] = kkp['email']
        result['fax'] = kkp['fax']
        result['actived'] = actived

        return result

    def count(self, typeid="", officeid=""):
        param = 'typeid={}&officeid={}'.format(typeid, officeid)
        return requests.get('{}/{}/count?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, typeid="", officeid=""):
        param = 'typeid={}&officeid={}'.format(typeid, officeid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def all_kkp(self):
        return requests.get('{}/{}/allkkp'.format(self.host, self.root), headers=self.header)

    def kkp(self, officeid=""):
        param = 'officeid={}'.format(officeid)
        return requests.get('{}/{}/kkp?{}'.format(self.host, self.root, param), headers = self.header)

    def add(self, office={}):
        djson = {'office': office}
        return requests.post('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def update(self, office={}):
        djson = {'office': office}
        return requests.put('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def delete(self, officeid=""):
        djson = {'officeid': officeid}
        return requests.delete('{}/{}'.format(self.host, self.root), json=djson, headers=djson)
