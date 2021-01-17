import requests
import datetime

# Model
from model.base import BaseModel
from model.crud import CRUDModel

class OfficeModel(BaseModel):

    def __init__(self, collection:None, service:None):
        super().__init__(collection=collection, service=service)


    def kkp(self):
        return requests.get('{}/offices'.format(self.service))

    def find_kkp(self, officeid:str):
        return requests.get('{}/offices/find'.format(self.service), params={"officeid": officeid})


    def find_counter(self, officeid: str, counter: str):
        return CRUDModel(collection=self.collection).find(filter={"_id": officeid, "counter.key": counter }, field={"counter.$": 1}, session=session)

    def add_counter(self, officeid:str, session:None):
        return CRUDModel(collection=self.collection).update(filter={"officeid": officeid}, schema={"$push": {"counter": self.schema_counter}}, session=session)

    def delete_counter(self, officeid: str, counter: str, session: None):
        return CRUDModel(collection=self.collection).update(filter={"_id": officeid}, schema={"$pull": {"counter": {"key": counter}}}, session=session)

    def booking(self, officeid: str, counter: str, session: None):
        office = CRUDModel(collection=self.collection).find(filter={"_id": officeid, "counter.key": counter }, field={"counter.$": 1}, session=session)
        new_counter = {"counter.$.value": office['counter'][0]['value']+1, "counter.$.updatedate": datetime.datetime.now()}
        CRUDModel(collection=self.collection).update(filter={"$and": [{"_id": officeid}, {"counter.key": counter}]}, schema={"$set": new_counter}, session=session)

        return office['counter'][0]['value']
