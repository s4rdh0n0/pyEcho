import requests

# Model
from model.base import BaseModel


class RegionModel (BaseModel):

    root = 'offices/region'

    def __init__(self, officeid="", officetypeid=""):
        self.officeid = officeid
        self.officetypeid = officetypeid

    def get_provinsi(self) -> requests.Response:
        param = 'officeid={}&officetypeid={}'.format(self.officeid, self.officetypeid)
        return requests.get('{}/{}/provinsi?{}'.format(self.host, self.root, param), headers=self.header)

    def get_kabupaten(self, parent="") -> requests.Response:
        param = 'kabupatenid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/kabupaten?{}'.format(self.host, self.root, param), headers=self.header)
        

    def get_kecamatan(self, parent="", ) -> requests.Response:
        param = 'kecamatanid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/kecamatan?{}'.format(self.host, self.root, param), headers=self.header)
        

    def get_desa(self, parent="") -> requests.Response:
        param = 'desaid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        return requests.get('{}/{}/desa?{}'.format(self.host, self.root, param), headers=self.header)
        
