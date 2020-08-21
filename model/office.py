import requests

from model.base import BaseModel


class OfficeModel(BaseModel):

    def __init__(self):
        pass

    def get_all(self):
        response = requests.get('{}/offices'.format(self.host), headers=self.get_header())

        return response

    def find(self, officeid=""):
        param = 'officeid={}'.format(officeid)
        response = requests.get('{}/offices/find?{}'.format(self.host, param), headers=self.host)

        return response