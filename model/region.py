import requests

from model.base import BaseModel


class RegionModel (BaseModel):

    def __init__(self, officeid="", officetypeid=""):
        self.officeid = officeid
        self.officetypeid = officetypeid

    def get_provinsi(self) -> requests.Response:
        param = 'officeid={}&officetypeid={}'.format(self.officeid, self.officetypeid)
        response = requests.get('{}/offices/region/provinsi?{}'.format(self.host, param), headers=self.get_header())

        return response

    def get_kabupaten(self, parent="") -> requests.Response:
        param = 'kabupatenid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        response = requests.get('{}/offices/region/kabupaten?{}'.format(self.host, param), headers=self.get_header())
        
        return response

    def get_kecamatan(self, parent="", ) -> requests.Response:
        param = 'kecamatanid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        response = requests.get('{}/offices/region/kecamatan?{}'.format(self.host, param), headers=self.get_header())
        
        return response

    def get_desa(self, parent="") -> requests.Response:
        param = 'desaid={}&officeid={}&officetypeid={}'.format(parent, self.officeid, self.officetypeid)
        response = requests.get('{}/offices/region/desa?{}'.format(self.host, param), headers=self.get_header())
        
        return response
