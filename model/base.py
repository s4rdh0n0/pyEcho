import requests

# Tornado Framework
import tornado.web
from tornado.options import options, define


class BaseModel():

    def __init__(self, host="", token=""):
        self.host = host
        self.token = token
        self.__header = {'Authorization': 'Bearer {}'.format(self.token)}


    def get_header(self):
        return self.__header
