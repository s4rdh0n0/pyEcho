import requests
import datetime

# Model
from model.base import BaseModel

class NodeModel(BaseModel):
    
    schema = {'_id': None,
             'register': None,
             'berkasid': None,
             'operator': None,
             'type': None,
             'sender': None,
             'senddate': None,
             'startdate': None,
             'finnishdate': None,
             'status': False}


    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, filter:{}, page_size:int, page_num:int):
        skips = page_size * (page_num - 1)
        cursor = self.collection.find(filter).skip(skips).limit(page_size)

        return [x for x in cursor]