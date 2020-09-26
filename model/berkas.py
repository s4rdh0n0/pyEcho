import requests

# Model
from model.base import BaseModel


class BerkasModel(BaseModel):

    root = 'offices/berkas'

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)

    def pagination(self, nomor="", tahun="", draw="", start="", limit=""):
        param = 'officeid={}&nomor={}&tahun={}&start={}&limit={}&count={}'.format(self.officeid, nomor, tahun, start, limit, "-1")
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def search(self, nomor="", tahun=""):
        param = 'officeid={}&nomor={}&tahun={}&start={}&limit={}&count={}'.format(self.officeid, nomor, tahun, "0", "1", "-1")
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)
        if response.status_code == 200:
            return {'status': True, 'data': response.json()}
        else:
            return {'status': False, 'data': ""}

    def find(self, berkasid=""):
        param =  'berkasid={}'.format(berkasid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def simponi(self, berkasid=""):
        param = 'berkasid={}'.format(berkasid)
        return requests.get('{}/{}/simponi?{}'.format(self.host, self.root, param), headers=self.header)

    def daftarisian(self, berkasid=""):
        param = 'berkasid={}'.format(berkasid)
        return requests.get('{}/{}/di?{}'.format(self.host, self.root, param), headers=self.header)

    def produk(self, berkasid=""):
        param = 'berkasid={}'.format(berkasid)
        return requests.get('{}/{}/produk?{}'.format(self.host, self.root, param), headers=self.header)

    def blanko(self, berkasid=""):
        param = 'berkas={}'.format(berkasid)
        return requests.get('{}/{}/blanko?{}'.format(self.host, self.root, param), headers=self.header)
