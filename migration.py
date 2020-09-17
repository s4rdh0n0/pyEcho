import uuid

# Tornado
import tornado.gen

# Model
from model.office import OfficeModel
from model.user import UserModel
from model.master import MasterModel


config = {
    'HOST': 'http://localhost:8000',
    'TOKEN': None,
    'OFFICEID': 'd8af2d0372b84f6fb33a97847b94cacd'
}


def token():
    user = UserModel(officeid=None, host=config['HOST'], token=None)
    result = user.auth(username="s4rdh0n0", password="4231Dodon")
    return result.json()

def master():
    role = MasterModel(type="typerole", host=config['HOST'], token=token()['token'])

    if role.find(code='REGIN').status_code == 400:
        schema = role.schema
        schema['_id'] = uuid.uuid4().__str__()
        schema['type'] = role.type
        schema['code'] = 'REGIN'
        schema['description'] = 'Register Berkas Masuk'
        schema['actived'] = True
        print("Insert {}: {}".format(schema['description'], role.add(master=schema)))

    if role.find(code='REGOUT').status_code == 400:
        schema = role.schema
        schema['_id'] = uuid.uuid4().__str__()
        schema['type'] = role.type
        schema['code'] = 'REGOUT'
        schema['description'] = 'Register Berkas Keluar'
        schema['actived'] = True
        print("Insert {}: {}".format(schema['description'], role.add(master=schema)))

    if role.find(code='SURVEY').status_code == 400:
        schema = role.schema
        schema['_id'] = uuid.uuid4().__str__()
        schema['type'] = role.type
        schema['code'] = 'SURVEY'
        schema['description'] = 'Petugas Ukur'
        schema['actived'] = True
        print("Insert {}: {}".format(schema['description'], role.add(master=schema)))

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
    office()
    master()
