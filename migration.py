import uuid

# Tornado
import tornado.gen

# Model
from model.office import OfficeModel
from model.user import UserModel
from model.master import MasterModel


config = {
    'HOST': 'http://localhost:8000'
}


def token():
    user = UserModel(officeid=None, host=config['HOST'], token=None)
    result = user.auth(username="s4rdh0n0", password="4231Dodon")
    return result.json()

def user():
    pass

def role():
    role = MasterModel(host=config['HOST'], token=token()['token'])

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'REGIN'
    schema['description'] = 'Register Berkas Masuk'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'REGOUT'
    schema['description'] = 'Register Berkas Keluar'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'SURVEY'
    schema['description'] = 'Petugas Ukur'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'DRAWING'
    schema['description'] = 'Petugas Penggambaran dan Pemetaan'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'MANAGER'
    schema['description'] = 'Koreksi dan Validasi Berkas dan Document'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'ADMINISTRATOR'
    schema['description'] = 'Pengelola Aplikasi dan Data'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

def office():
    office = OfficeModel(host=config['HOST'], token=token()['token'])
    offices = office.all_kkp()
    if offices.status_code == 200:
        for o in offices.json()['result']:
            if o['code'] == '1228':
                print("{} - {}".format(o['code'], o['name']))

                schema_office = office.kkpTooffice(officeid=o['officeid'],kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
                office.add(office=schema_office)

                if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
                    register = office.counter_schema
                    register['key'] = 'REGISTER'
                    register['value'] = 0
                    register['actived'] = True
                    office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

                if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
                    document = office.counter_schema
                    document['key'] = 'DOCUMENT'
                    document['value'] = 0
                    document['actived'] = True
                    office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

                if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
                    tools = office.counter_schema
                    tools['key'] = 'TOOL'
                    tools['value'] = 0
                    tools['actived'] = True
                    office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

    else:
        print('Error: Response not found.')



if __name__ == "__main__":
    # office()
    role()
