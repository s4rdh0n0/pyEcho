import requests

# Model
from model.base import BaseModel


class UserModel(BaseModel):

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)

    def count(self, userid=""):
        if userid == "":
            param = 'officeid=' + self.officeid
        else:
            param = 'officeid={}&userid={}'.format(self.officeid, userid)

        return requests.get('{}/offices/users/count?{}'.format(self.host, param), headers=self.header)

    def get_user(self, db="", type="", id=""):
        param = 'officeid={}&type={}&id={}&db={}'.format(self.officeid, type, id, db)

        return requests.get('{}/{}{}'.format(self.host, 'offices/users/find?', param), headers=self.header)


    def set_user(self, username=""):
        user = self.get_user(db="kkp", type="username", id=username)
        if user.status_code == 200:
            count = self.count(userid=user.json()['result']['userid'])
            if count.status_code == 200:
                if count.json()['result'] == 0:
                    param = {'officeid': self.officeid, 'username': username}
                    request = requests.post('{}/{}'.format(self.host, 'offices/users/add'), json=param, headers=self.header)

                    return {'status': True, 'data': request.json(), 'type': 'info', 'msg': 'Data pegawai berhasil disimpan.'}
                else:
                    return {'status': False, 'data': None, 'type': 'warning', 'msg': 'Pegawai sudah terdaftar pada database.'}
            else:
                return {'status': False, 'data': None, 'type': 'danger', 'msg': 'Server not response.'}
        else:
            return {'status': False, 'data': None, 'type': 'danger', 'msg': 'Server not response.'}


    def get_all(self, pegawaiid="", draw=0, page=0, limit=0, start=0):
        record = self.count(userid="")
        if record.status_code == 200:
            param = 'officeid={}&pegawaiid={}&limit={}&page={}'.format(self.officeid, pegawaiid, limit, page)
            users = requests.get('{}/{}{}'.format(self.host, 'offices/users?', param), headers=self.header)
            if users.status_code == 200:
                if users.json()['result'] != None:
                    return {'status': True, 'draw': draw, 'data': users.json()['result'], 'recordsTotal': record.json()['result'], 'recordsFiltered': record.json()['result']}
                else:
                    return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
        else:
            return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
