import requests

# Model
from model.base import BaseModel
from model.master import MasterModel

class UserModel(BaseModel):
    
    root = 'offices/users'

    schema = {
        '_id': None,
        'username': None,
        'officeid': None, 
        'pegawaiid': None,
        'nama': None,
        'role': [],
        'createdate': None, 
        'actived': False,
    }

    role_schema = {
        'key': None,
        'createdate': None,
        'usercreate': None,
        'description': None,
    }

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)

    def auth(self, username="", password=""):
        djson = {"username": username, "password": password}
        return requests.post('{}/{}'.format(self.host, 'auth/login'), json=djson)

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
    
    # Convert schema kkp to schema locals
    def kkpToUser(self, officeid="", kkp={}, actived=False):
        result = self.schema
        result['officeid'] = officeid
        result['pegawaiid'] = kkp['pegawaiid']
        result['username'] = kkp['username']
        result['nama'] = kkp['nama']
        result['actived'] = actived

        return result

    def count(self, typeid="", userid=""):
        if userid == "" or typeid == "":
            param = 'officeid=' + self.officeid
        else:
            param = 'officeid={}&typeid={}&userid={}'.format(self.officeid, typeid, userid)
            
        return requests.get('{}/{}/count?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, typeid="", userid=""):
        param = 'typeid={}&userid={}'.format(typeid, userid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def entity(self, username=""):
        param = 'officeid={}&username={}'.format(self.officeid, username)
        return  requests.get('{}/{}/kkp/entity?{}'.format(self.host, self.root, param), headers=self.header)

    def entityfoto(self, pegawaiid=""):
        param = 'pegawaiid={}'.format(pegawaiid)
        return requests.get('{}/{}/foto?{}'.format(self.host, self.root, param), headers=self.header)

    def pegawai(self, username=""):
        param = 'username={}'.format(username)
        return requests.get('{}/{}/kkp/pegawai?{}'.format(self.host, self.root, param), headers=self.header)

    def add(self, user={}):
        djson = {'officeid': self.officeid,
                 'user': user}

        return requests.post('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def update(self, user={}):
        djson = {'officeiid': self.officeid,
                 'user': user}

        return requests.put('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def delete(self, typeid="", userid=""):
        djson = {'typeid': typeid,
                 'userid': userid}

        return requests.delete('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def role(self, typeid="", userid=""):
        param = 'typeid={}&userid={}'.format(typeid, userid)
        response = requests.get('{}/{}/role?{}'.format(self.host, self.root, param), headers=self.header)
        if response.status_code == 200:
            if response.json()['result'] != None:
                return {'status': True, 'draw': 0, 'data': response.json()['result'], 'recordsTotal': len(response.json()['result']), 'recordsFiltered': len(response.json()['result'])}
            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
        else:
            return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find_role(self, typeid="", userid="", key=""):
        param = 'typeid={}&userid={}&key={}'.format(typeid, userid, key)
        return requests.get('{}/{}/role/find?{}'.format(self.host, self.root, param), headers=self.header)

    def role_add(self, typeid="", userid="", role={}):
        djson = {'typeid': typeid,
                 'userid': userid,
                 'role': role}

        return requests.post('{}/{}/role'.format(self.host, self.root), json=djson, headers=self.header)

    def role_update(self, typeid="", userid="", role={}):
        param = {'typeid': '_id',
                 'userid': userid,
                 'role': role}
        
        return requests.put('{}/{}/role'.format(self.host, self.root), json=param, headers=self.header)

    def role_delete(self, userid="", key=""):
        param = {'typeid': '_id',
                 'userid': userid,
                 'key': key}

        return requests.delete('{}/{}/role'.format(self.host, self.root), json=param, headers=self.header)

