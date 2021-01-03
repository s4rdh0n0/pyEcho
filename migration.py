import datetime
import uuid
import yaml


from model.base import ConnectionModel
from model.office import OfficeModel
from model.master import MasterModel


def InsertOffice():
    with open('migration.yaml') as f:
        config_docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in config_docs:
            client = ConnectionModel(username=doc['db']['username'],password=doc['db']['password'],server=doc['db']['server'],port=doc['db']['port'])
            
            collection = client.collection(database="registerdb", name="offices")
            office = OfficeModel(collection=collection, service="http://localhost:8000")

            for o in office.kkp().json()['result']:
                if o['code'] == doc['code']
                    
                    office.find_kkp(officeid=o['officeid'])


def InsertMaster():
    with open('migration.yaml') as f:
        config_docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in config_docs:
            client = ConnectionModel(username=doc['db']['username'],password=doc['db']['password'],server=doc['db']['server'],port=doc['db']['port'])
            
            collection = client.collection(database="registerdb", name="master")
            role = MasterModel(collection=collection, service=None)
            for m in doc['master']:
                schema = role.schema
                
                schema['_id'] = uuid.uuid4().__str__()
                schema['type'] = m['type']
                schema['code'] = m['code']
                schema['description'] = m['description']
                schema['createdate'] = datetime.datetime.now()
                schema['usercreate'] = '6ad05c0a-daac-4b3d-9c3e-997d5dff2124'
                schema['actived']
                if role.count(filter={"type": m['type'], "code": m['code']}) == 0:
                    role.add(schema=schema)
                    
                print("=> {} : OK".format(m['description']))




InsertOffice()

InsertMaster()
