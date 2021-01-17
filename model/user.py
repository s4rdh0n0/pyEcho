import requests
import datetime

# Model
from model.base import BaseModel
from model.crud import CRUDModel


class UserModel(BaseModel):
    schema = {
        '_id': None,
        'username': None,
        'password': None,
        'officeid': None, 
        'pegawaiid': None,
        'nama': None,
        'email': None,
        'phone': None,
        'role': [],
        'createdate': None,
        'usercreate': None,
        'updatedate': None,
        'userupdate': None,
        'actived': False,
    }

    schema_role = {
        'key': None,
        'description': None,
        'startdate': None,
    }

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def auth(self, username:str, password:str, session:None):
        count = CRUDModel(collection=self.collection).count(filter={"username": username, "password": password, "actived": True}, session=session)
        if count > 0:
            return True
        else:
            return False

    # Service
    def kkp(self, officeid:str, username:str):
        return  requests.get('{}/offices/user'.format(self.service), params={"officeid": officeid, "username": username})

    def kkp_foto(self, pegawaiid=""):
        return requests.get('{}/offices/user/foto'.format(self.service), params={"pegawaiid": pegawaiid})


    def pagination(self, filter:{}, page_size:int, page_num:int):
        skips = page_size * (page_num - 1)
        cursor = self.collection.find(filter).skip(skips).limit(page_size)

        return [x for x in cursor]

    def find_role(self, userid:str, role:str, session: None):
        return CRUDModel(collection=self.collection).find(filter={"_id": userid, "role.key": role}, field={"role.$": 1}, session=None)

    def add_role(self, userid:str, schema:{}, session: None):
        return CRUDModel(collection=self.collection).update(filter={"_id": userid}, schema={"$push": {"role": schema}}, session=None)

    def delete_role(self, userid: str, role: str, session: None):
        return CRUDModel(collection=self.collection).update(filter={"_id": userid}, schema={"$pull": {"role": {"key": role}}}, session=None)
