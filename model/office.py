import requests

# Model
from model.base import BaseModel


class OfficeModel(BaseModel):

    root = 'offices'

    def __init__(self, host="", token=""):
        super().__init__(host=host, token=token)

    def get_all(self):
        response = requests.get('{}/{}'.format(self.host, self.root), headers=self.header)
        return response

    def find(self, officeid=""):
        param = 'officeid={}'.format(officeid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root,param), headers=self.host)