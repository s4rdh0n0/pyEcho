import requests

# Model
from model.base import BaseModel


class OfficeModel(BaseModel):

    root = 'offices'

    schema = {'_id': None,
             'code': None,
             'officetypeid': None,
             'parent': None,
             'nama': None,
             'kota': None,
             'alamat': None,
             'phone': None,
             'email': None,
             'fax': None,
             'counter': [],
             'actived': False}

    counter_schema = {'key': None,
                      'value': 0,
                      'actived': False}

    def __init__(self, host="", token=""):
        super().__init__(host=host, token=token)

    def all(self):
        return requests.get('{}/{}'.format(self.host, self.root), headers=self.header)

    def kkpTooffice(self, officeid="", kkp={}, actived=False):
        result = self.schema
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
        return requests.get('{}/{}/kkp/all'.format(self.host, self.root), headers=self.header)

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
        return requests.delete('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def all_counter(self, typeid="", officeid=""):
        param = 'type={}&officeid={}'.format(typeid, officeid)
        return requests.get('{}/{}/counter?{}'.format(self.host, self.root, param), headers=self.header)

    def counter(self, typeid="", officeid="", counterid=""):
        param = 'typeid={}&officeid={}&key={}'.format(typeid, officeid, counterid)
        return requests.get('{}/{}/counter/find?{}'.format(self.host, self.root, param), headers=self.header)

    def add_counter(self, typeid="", officeid="",counter={}):
        djson = {'typeid': typeid,
                 'officeid': officeid,
                 'counter': counter}

        return requests.post('{}/{}/counter'.format(self.host, self.root), json=djson, headers=self.header)

    def update_counter(self, typeid="", officeid="", counter={}):
        djson = {'typeid': typeid,
                 'officeid': officeid,
                 'counter': counter}

        return requests.put('{}/{}/counter'.format(self.host, self.root), json=djson, headers=self.header)

    def delete_counter(self, typeid="", officeid="", counterid=""):
        djson = {'typeid': typeid,
                 'officeid': officeid,
                 'key': counterid}

        return requests.delete('{}/{}/counter'.format(self.host, self.root), json=djson, headers=self.header)
