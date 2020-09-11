import requests

# Model
from model.base import BaseModel
from model.master import MasterModel

class UserModel(BaseModel):
    
    root = 'users'

    user_schema = {
        '_id': None,
        'username': None,
        'officeid': None, 
        'pegawaiid': None, 
        'nama': None,
        'phone': None,
        'email': None,
        'createdate': None, 
        'updatedate': None,
        'actived': None,
    }

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)

    def schema(self):
        return requests.get('{}/{}/schema'.format(self.host, self.root), headers=self.header)

    def schemarole(self):
        return requests.get('{}/{}/role/schema'.format(self.host, self.root), headers=self.header)

    def count(self, typeid="", userid=""):
        if userid == "":
            param = 'officeid=' + self.officeid
        else:
            param = 'officeid={}&typeid={}&userid={}'.format(self.officeid, typeid, userid)
            
        return requests.get('{}/{}/count?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, typeid="", userid=""):
        param = 'typeid={}&userid={}'.format(typeid, userid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def kkp(self, username=""):
        param = 'officeid={}&username={}'.format(self.officeid, username)
        return  requests.get('{}/{}/kkp?{}'.format(self.host, self.root, param), headers=self.header)

    def pagination(self, pegawaiid="", draw=0, page=0, limit=0, start=0):
        record = self.count(typeid="pegawaiid", userid=pegawaiid)
        if record.status_code == 200:
            param = 'officeid={}&pegawaiid={}&limit={}&page={}'.format(self.officeid, pegawaiid, limit, page)
            users = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)
            if users.status_code == 200:
                if users.json()['result'] != None:
                    return {'status': True, 'draw': draw, 'data': users.json()['result'], 'recordsTotal': record.json()['result'], 'recordsFiltered': record.json()['result']}
                else:
                    return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
    
    def add(self, data={}):
        param = {'officeid': self.officeid, 'user': data}
        return requests.post('{}/{}'.format(self.host, self.root), json=param, headers=self.header)

    def update(self, data={}):
        param = {'officeiid': self.officeid, 'user': data}
        return requests.put('{}/{}'.format(self.host, self.root), json=param, headers=self.header)
    
    def role(self, userid=""):
        param = 'typeid={}&userid={}'.format("_id", userid)
        response = requests.get('{}/{}/role?{}'.format(self.host, self.root, param), headers=self.header)
        if response.status_code == 200:
            if response.json()['result'] != None:
                return {'status': True, 'draw': 0, 'data': response.json()['result'], 'recordsTotal': len(response.json()['result']), 'recordsFiltered': len(response.json()['result'])}
            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
        else:
            return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def role_add(self, userid="", role={}):
        param = {'typeid': '_id',
                 'userid': userid,
                 'role': role}
        return requests.post('{}/{}/role'.format(self.host, self.root), json=param, headers=self.header)

    def role_delete(self, userid="", roleid=""):
        param = {'typeid': '_id',
                 'userid': userid,
                 'roleid': roleid}
        return requests.delete('{}/{}'.format(self.host, self.root), json=param, headers=self.header)


def TestingUser():
    auth_param = {
        'username': 's4rdh0n0',
        'password': '4231Dodon'
    }
    auth = requests.post('{}/{}/{}'.format("http://localhost:8000", 'auth', 'login'), json=auth_param)
    token = auth.json()['result']['token']

    print(token)
    # user = UserModel(officeid="", host="http://localhost:8000", token=token)


TestingUser()
