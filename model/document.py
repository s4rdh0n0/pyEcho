import requests

# Model
from model.base import BaseModel


class PersilModel(BaseModel):
    host = 'http://localhost:8000'
    root = 'office/document/persil'

    def __init__(self, officeid="", desaid="", host="", token=""):
        self.officeid = officeid
        self.desaid = desaid
        super().__init__(host=host, token=token)

    
    def pagination(self, nib="", draw="", start="", limit=""):
        param = 'officeid={}&desaid={}&nib={}&start={}&limit={}&count={}'.format(self.officeid, self.desaid, nib, start, limit, -1)
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, persilid=""):
        param = 'persilid={}'.format(persilid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class SuratUkurModel(BaseModel):

    root = 'office/document/suratukur'

    def __init__(self, officeid="", desaid="", host="", token=""):
        self.officeid = officeid
        self.desaid = desaid
        super().__init__(host=host, token=token)

    def pagination(self, typesu="", nomor="", tahun="", draw="", start="", limit=""):
        param = 'officeid={}&desaid={}&typesu={}&nomor={}&tahun={}&start={}&limit={}&count={}'.format(self.officeid, self.desaid, typesu, nomor, tahun, start, limit, "-1")
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, suratukurid=""):
        param = 'suratukurid={}'.format(suratukurid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class BukuTanahModel(BaseModel):

    root = 'office/document/bukutanah'

    def __init__(self, officeid="",  desaid="", host="", token=""):
        self.officeid = officeid
        self.desaid = desaid
        super().__init__(host=host, token=token)

    def pagination(self, typehak="", nomor="", draw="", start="", limit=""):
        param = 'officeid={}&desaid={}&typehak={}&nomor={}&start={}&limit={}&count={}'.format(self.officeid, self.desaid, typehak, nomor, start, limit, "-1")
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, bukutanahid=""):
        param = 'bukutanahid={}'.format(bukutanahid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class GambarUkurModel(BaseModel):

    root = 'office/document/gambarukur'

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        self.host = host
        super().__init__(host=host, token=token)

    def pagination(self, nomor="", tahun="", draw="", start="", limit=""):
        param = "officeid={}&nomor={}&tahun={}&start={}&limit={}&count={}".format(self.officeid, nomor, tahun, start, limit, -1)
        response = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, dokumenpengukuranid=""):
        param = 'dokumenpengukuranid={}'.format(dokumenpengukuranid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class STPModel(BaseModel):

    root = 'root/document/stp'

    def __init__(self, host="", token=""):
        self.host = host
        super().__init__(host=host)

    def find(self, stpid=""):
        param = 'stpid={}'.format(stpid)

        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)
