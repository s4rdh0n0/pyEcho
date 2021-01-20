import datetime
import uuid
import yaml


from model.base import ConnectionModel
from model.office import OfficeModel
from model.user import UserModel
from model.master import MasterModel


def InsertOffice(connection: None, document: None):
    office = OfficeModel(collection=connection.collection(database="pyDatabase", name="offices"), service="http://localhost:8000")
    master = MasterModel(collection=connection.collection(database="pyDatabase", name="master"), service=None)
    for d in document['office']:
        print("=> {}".format(d['kantah']))
        if office.count(filter={"code": d['code']}) == 0:
            for o in office.kkp().json()['result']:
                if o['code'] == d['code']:
                    profile_office_kkp = office.find_kkp(officeid=o['officeid']).json()['result']
                    counter = master.get(filter={"code": "REG", "type": "COUNTER"})
                    row_counter = dict()
                    row_counter['key'] = counter['code']
                    row_counter['value'] = 1
                    row_counter['createdate'] = datetime.datetime.now()

                    row_office = dict()
                    row_office['_id'] = o['officeid']
                    row_office['code'] = o['code']
                    row_office['parent'] = profile_office_kkp['parent']
                    row_office['officetypeid'] = profile_office_kkp['officetypeid']
                    row_office['nama'] = profile_office_kkp['name']
                    row_office['kota'] = profile_office_kkp['city']
                    row_office['alamat'] = profile_office_kkp['address']
                    row_office['phone'] = profile_office_kkp['phone']
                    row_office['email'] = profile_office_kkp['email']
                    row_office['counter'] = [row_counter]
                    row_office['actived'] = True

                    office.add(schema=row_office)


def InsertUser(connection: None, document: None):
    master = MasterModel(collection=connection.collection(database="pyDatabase", name="master"), service=None)
    user = UserModel(collection= connection.collection(database="pyDatabase", name="users"), service="http://localhost:8000")
    for d in document['user']:
        print("=> {}".format(d['username']))
        if user.count(filter={"username": d['username']}) == 0:
            kkp = user.kkp(officeid=d['officeid'], username=d['username']).json()['result']
            
            row_role_admin = dict()
            row_role_admin['key'] = 'ADMINISTRATOR'
            row_role_admin['description'] = master.get(filter={"type": "JOB", "code": "ADMINISTRATOR"})['description']
            row_role_admin['startdate'] = datetime.datetime.now()

            row_role_regin = dict()
            row_role_regin = {}
            row_role_regin['key'] = 'REGIN'
            row_role_regin['description'] = master.get(filter={"type": "JOB", "code": "REGIN"})['description']
            row_role_regin['startdate'] = datetime.datetime.now()       

            row = dict()
            row["_id"] = kkp['userid']
            row["username"] = d['username']
            row["password"] = 'trenggalek1'
            row["officeid"] = d['officeid']
            row["pegawaiid"] = kkp['pegawaiid']
            row["nama"] = kkp['nama']
            row["email"] = d['email']
            row["phone"] = kkp['phone']
            row["role"] = [row_role_admin, row_role_regin]
            row["createdate"] = datetime.datetime.now()
            row["usercreate"] = kkp['userid']
            row["actived"] = True


            user.add(schema=row)


def InsertMaster(connection: None, document: None):
    role = MasterModel(collection=connection.collection(database="pyDatabase", name="master"), service=None)
    for m in document['master']:
        row_master = dict()
        row_master['_id'] = uuid.uuid4().__str__()
        row_master['type'] = m['type']
        row_master['code'] = m['code']
        row_master['description'] = m['description']
        row_master['createdate'] = datetime.datetime.now()
        row_master['usercreate'] = '6ad05c0a-daac-4b3d-9c3e-997d5dff2124'
        row_master['actived'] = True
        if role.count(filter={"type": m['type'], "code": m['code']}) == 0:
            role.add(schema=row_master)
            
        print("=> {} : OK".format(m['description']))




with open('migration.yaml') as f:
    config_docs = yaml.load_all(f, Loader=yaml.FullLoader)
    for doc in config_docs:
        _connection = ConnectionModel(username=doc['db']['username'],password=doc['db']['password'],server=doc['db']['server'],port=doc['db']['port'])
        InsertMaster(connection=_connection, document=doc)
        InsertOffice(connection=_connection, document=doc)
        InsertUser(connection=_connection, document=doc)
