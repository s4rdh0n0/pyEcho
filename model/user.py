import requests

# Model
from model.base import BaseModel


class UserModel(BaseModel):
    
    root = 'offices/users'

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        self.role = self.RoleModel(host=host, token=token)
        super().__init__(host=host, token=token)

    def get_schema(self):
        return requests.get('{}/{}/schema'.format(self.host, self.root), headers=self.header)

    def get_count(self, userid=""):
        if userid == "":
            param = 'officeid=' + self.officeid
        else:
            param = 'officeid={}&userid={}'.format(self.officeid, userid)
        return requests.get('{}/offices/users/count?{}'.format(self.host, param), headers=self.header)

    def get_user(self, db="", type="", id=""):
        param = 'officeid={}&type={}&id={}&db={}'.format(self.officeid, type, id, db)
        return requests.get('{}/{}{}'.format(self.host, 'offices/users/find?', param), headers=self.header)

    def get_all(self, pegawaiid="", draw=0, page=0, limit=0, start=0):
        record = self.get_count(userid="")
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
        else:
            return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def add_user(self, data={}):
        param = {'officeid': self.officeid, 'user': data}
        return requests.post('{}/{}/add'.format(self.host, self.root), json=param, headers=self.header)

    def update_user(self, data={}):
        param = {'officeiid': self.officeid, 'user': data}
        return requests.put('{}/{}/update'.format(self.host, self.root), json=param, headers=self.header)

    
    class RoleModel(BaseModel):

        root = 'offices/users/role'

        def __init__(self, host="", token=""):
            super().__init__(host=host, token=token)

        def get_schema(self):
            return requests.get('{}/{}/schema'.format(self.host, self.root), headers=self.header)

        def get_role(self, userid=""):
            param = 'userid={}'.format(userid)
            return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

        def get_status(self, userid="", code=""):
            pass
