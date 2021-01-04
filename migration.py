import datetime
import uuid
import yaml


from model.base import ConnectionModel
from model.office import OfficeModel
from model.user import UserModel
from model.master import MasterModel


def InsertOffice():
    with open('migration.yaml') as f:
        config_docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in config_docs:
            client = ConnectionModel(username=doc['db']['username'],password=doc['db']['password'],server=doc['db']['server'],port=doc['db']['port'])
            
            col_office = client.collection(database="registerdb", name="offices")
            col_master = client.collection(database="registerdb", name="master")

            office = OfficeModel(collection=col_office, service="http://localhost:8000")
            master = MasterModel(collection=col_master, service=None)
            for d in doc['office']:
                print("=> {}".format(d['kantah']))
                if office.count(filter={"code": d['code']}) == 0:
                    for o in office.kkp().json()['result']:
                        if o['code'] == d['code']:
                            profile = office.find_kkp(officeid=o['officeid']).json()['result']
                            counter = master.get(filter={"code": "REG", "type": "COUNTER"})

                            schema_counter = office.schema_counter
                            schema_counter['key'] = counter['code']
                            schema_counter['value'] = 1
                            schema_counter['createdate'] = datetime.datetime.now()

                            schema = office.schema
                            schema['_id'] = o['officeid']
                            schema['code'] = o['code']
                            schema['parent'] = profile['parent']
                            schema['officetypeid'] = profile['officetypeid']
                            schema['nama'] = profile['name']
                            schema['kota'] = profile['city']
                            schema['alamat'] = profile['address']
                            schema['phone'] = profile['phone']
                            schema['email'] = profile['email']
                            schema['counter'] = [schema_counter]
                            schema['actived'] = True

                            office.add(schema=schema)



def InsertUser():
    with open('migration.yaml') as f:
        config_docs = yaml.load_all(f, Loader=yaml.FullLoader)
        for doc in config_docs:
            client = ConnectionModel(username=doc['db']['username'],password=doc['db']['password'],server=doc['db']['server'],port=doc['db']['port'])
            
            col_user = client.collection(database="registerdb", name="users")
            col_master = client.collection(database="registerdb", name="master")

            master = MasterModel(collection=col_master, service=None)
            user = UserModel(collection=col_user, service="http://localhost:8000")
            for d in doc['user']:
                print("=> {}".format(d['username']))
                if user.count(filter={"username": d['username']}) == 0:
                    kkp = user.kkp(officeid=d['officeid'], username=d['username']).json()['result']
                    
                    role_admin = {}
                    role_admin['key'] = 'ADMINISTRATOR'
                    role_admin['description'] = master.get(filter={"type": "ROLE", "code": "ADMINISTRATOR"})['description']
                    role_admin['startdate'] = datetime.datetime.now()

                    role_regin = {}
                    role_regin['key'] = 'REGIN'
                    role_regin['description'] = master.get(filter={"type": "ROLE", "code": "REGIN"})['description']
                    role_regin['startdate'] = datetime.datetime.now()           

                    schema = user.schema
                    schema["_id"] = kkp['userid']
                    schema["username"] = d['username']
                    schema["password"] = 'trenggalek1'
                    schema["officeid"] = d['officeid']
                    schema["pegawaiid"] = kkp['pegawaiid']
                    schema["nama"] = kkp['nama']
                    schema["email"] = d['email']
                    schema["phone"] = kkp['phone']
                    schema["role"] = [role_admin, role_regin]
                    schema["createdate"] = datetime.datetime.now()
                    schema["usercreate"] = kkp['userid']
                    schema["actived"] = True


                    user.add(schema=schema)




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



InsertMaster()

InsertOffice()

InsertUser()
