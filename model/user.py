import requests

from model.base import BaseModel


class UserModel(BaseModel):


    def __init__(self, officeid = ""):
        self.officeid = officeid

    def count(self, userid=""):
        if userid =="":
            param = 'officeid=' + self.officeid
        else:
            param = 'officeid={}&userid={}'.format(self.officeid, userid)

        response = requests.get('{}/offices/find?{}'.format(self.host, param), headers=self.get_header())

        return response

    def get_user(self):
        pass

    def get_all(self, pegawaiid="", draw=0, page=0, limit=0, start=0):
        record = self.count(userid="")
        if record.status_code == 200:
            param = 'officeid={}&pegawaiid={}&limit={}&page={}'.format(self.officeid, pegawaiid, limit, page)
            users = requests.get('{}/{}{}'.format(self.host, 'offices/users?', param), headers=self.get_header())
            if users.status_code == 200:
                if users.json()['result'] != None:
                    return {'status': True, 'draw': draw, 'data': users.json()['result'], 'recordsTotal': record.json()['result'], 'recordsFiltered': record.json()['result']}
                else:
                    return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
        else:
            return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
