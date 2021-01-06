import requests

# Model
from model.base import BaseModel


class BerkasModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, officeid:str, nomor:str, tahun:str, draw:str, start:str, limit:str):
        response = requests.get('{}/offices/berkas'.format(self.service), params={"officeid":officeid, "nomor":nomor, "tahun":tahun, "start":start, "limit": limit, "count": -1})

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def search(self, officeid:str, nomor:str, tahun:str):
        response = requests.get('{}/offices/berkas'.format(self.service), params={"officeid":officeid, "nomor":nomor, "tahun":tahun, "start":0, "limit": 1, "count": -1})
        if response.status_code == 200:
            return {'status': True, 'data': response.json()}
        else:
            return {'status': False, 'data': ""}

    def find(self, berkasid:str):
        return requests.get('{}/offices/berkas/find'.format(self.service), params={"berkasid": berkasid})

    def simponi(self, berkasid:str):
        return requests.get('{}/offices/berkas/simponi'.format(self.service), params={"berkasid": berkasid})

    def daftarisian(self, berkasid:str):
        return requests.get('{}/offices/berkas/di'.format(self.service), params={"berkasid": berkasid})

    def produk(self, berkasid:str):
        return requests.get('{}/offices/berkas/produk'.format(self.service), params={"berkasid": berkasid})

    def blanko(self, berkasid:str):
        return requests.get('{}/offices/berkas/blanko'.format(self.service), params={"berkasid": berkasid})
