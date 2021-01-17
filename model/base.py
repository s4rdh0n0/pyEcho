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

    def add(self, schema: {}, session: None):
        return CRUDModel(collection=self.collection).insert(schema=schema, session=session)

    def update(self, filter: {}, schema: {}, session: None):
        return CRUDModel(collection=self.collection).update(filter=filter, schema={"$set": schema}, session=session)

    def delete(self, filter: {}, session: None):
        return CRUDModel(collection=self.collection).delete(filter=filter, session=session)


    def select(self, filter: {}, session: None):
        return CRUDModel(collection=self.collection).select(filter=filter, session=session)


    def get(self, filter: {}, session: None):
        return CRUDModel(collection=self.collection).find(filter=filter, field={}, session=session)

    def count(self, filter: {}, session: None):
        return CRUDModel(collection=self.collection).count(filter=filter, session=session)

class ConnectionModel():
    """
    docstring
    """
    
    def __init__(self, username:str, password:str, server:str, port: str):
        self.username = username
        self.password = password
        self.server = server
        self.port = port
        self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/'.format(username, password, server, port))

    def collection(self, database:str, name:str):
        db = self.client[database]
        return db[name]

