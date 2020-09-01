import requests

# Model
from model.base import BaseModel


class PersilModel(BaseModel):

    root = 'document/persil'

    def __init__(self, officeid="", desaid="", host="", token=""):
        self.officeid = officeid
        self.desaid = desaid
        super().__init__(host=host, token=token)

    
    def pagination(self, nib="", draw="", start="", limit=""):
        param = 'officeid={}&desaid={}&nib={}&start={}&limit={}&count={}'.format(self.officeid, self.desaid, nib, start, limit, -1)
        return requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, persilid=""):
        param = 'persilid={}'.format(persilid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class SuratUkurModel(BaseModel):

    root = 'document/suratukur'

    def __init__(self, officeid="", desaid="", host="", token=""):
        self.officeid = officeid
        self.desaid = desaid
        super().__init__(host=host, token=token)

    def pagination(self, typesu="", nomor="", tahun="", start="", limit=""):
        param = 'officeid={};desaid={};typesu={};nomor={};tahun={};start={};limit={};count={}'.format(self.officeid, self.desaid, typesu, nomor, tahun, start, limit, "-1")
        return requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)

    def find(self, suratukurid=""):
        param = 'suratukurid={}'.format(suratukurid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

class BukuTanahModel(BaseModel):

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)
