import requests

# Model
from model.base import BaseModel


class BerkasModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, filter: {}, page_size: int, page_num: int):
        skips = page_size * (page_num - 1)
        cursor = self.collection.find(filter).skip(skips).limit(page_size)

        return [x for x in cursor]

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
