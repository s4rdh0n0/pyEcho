import requests
import pymongo

from model.crud import CRUDModel


class BaseModel():
    """
    docstring
    """
    def __init__(self, collection: None, service: None):
        self.collection = collection
        self.service = service

    def pagination(self, page_size: int, page_num: int):
        return CRUDModel(collection=self.collection).pagination(page_size=page_size, page_num=page_num)

    def add(self, schema: {}):
        return CRUDModel(collection=self.collection).insert(schema=schema)

    def update(self, filter: {}, schema: {}):
        return CRUDModel(collection=self.collection).update(filter=filter, schema={"$set": schema})

    def delete(self, filter: {}):
        return CRUDModel(collection=self.collection).delete(filter=filter)


    def select(self, filter: {}):
        return CRUDModel(collection=self.collection).select(filter=filter)


    def get(self, filter: {}):
        return CRUDModel(collection=self.collection).find(filter=filter, field={})

    def count(self, filter: {}):
        return CRUDModel(collection=self.collection).count(filter=filter)

class ConnectionModel():
    """
    docstring
    """
    
    def __init__(self, username:str, password:str, server:str, port: str):
        self.username = username
        self.password = password
        self.server = server
        self.port = port

        self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}'.format(username, password, server, port))

    def collection(self, database:str, name:str):
        db = self.client[database]
        return db[name]

