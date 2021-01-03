import requests

# Model
from model.base import BaseModel


class RegionModel (BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def get_provinsi(self, officeid:str, officetypeid:str):
        return requests.get('{}/offices/region/provinsi'.format(self.service), params={"officeid":officeid, "officetypeid": officetypeid})

    def get_kabupaten(self, parent: str, officeid: str, officetypeid: str):
        return requests.get('{}/offices/region/kabupaten'.format(self.service), params={"provinsiid": parent,"officeid": officeid, "officetypeid": officetypeid})

    def get_kecamatan(self, parent: str, officeid: str, officetypeid: str):
        return requests.get('{}/offices/region/kecamatan'.format(self.service), params={"kabupatenid": parent, "officeid": officeid, "officetypeid": officetypeid})

    def get_desa(self, parent: str, officeid: str, officetypeid: str):
        return requests.get('{}/offices/region/desa'.format(self.service), params={"kecamatanid": parent, "officeid": officeid, "officetypeid": officetypeid})

    def all_desa(self, officeid:str):
        return requests.get('{}/offices/region/desa/all'.format(self.service), params={"officeid": officeid})
        
    def desa(self, kode=""):
        data = self.all_desa()
        for desa in data.json()['result']:
            if desa['code'] == kode:
                return desa
