import requests

# Model
from model.base import BaseModel


class MasterModel(BaseModel):
    
    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)
