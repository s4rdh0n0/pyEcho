import requests

# Model
from model.base import BaseModel


class MasterModel(BaseModel):


    root = 'offices/master'

    def __init__(self, type="", host="", token=""):
        self.type = type
        super().__init__(host=host, token=token)

    def get_master(self):
        param = 'type={}'.format(self.type)
        return  requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)
