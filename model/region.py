import requests

# Model
from model.base import BaseModel


class RegionModel (BaseModel):

    root = 'offices/region'

    def __init__(self, officeid="", officetypeid=""):
        self.officeid = officeid
        self.officetypeid = officetypeid

    def get_provinsi(self):
        param = 'officeid={}&officetypeid={}'.format(self.officeid, self.officetypeid)
        return requests.get('{}/{}/provinsi?{}'.format(self.host, self.root, param), headers=self.header)

    def get_kabupaten(self, parent=""):
        param = 'kabupatenid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/kabupaten?{}'.format(self.host, self.root, param), headers=self.header)    

    def get_kecamatan(self, parent="", ):
        param = 'kecamatanid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/kecamatan?{}'.format(self.host, self.root, param), headers=self.header)     

    def get_desa(self, parent=""):
        param = 'desaid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/desa?{}'.format(self.host, self.root, param), headers=self.header)
        
