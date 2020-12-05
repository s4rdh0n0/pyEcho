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
    result = user.auth(username="s4rdh0n0", password="YCxa2SJxLXQhFN")
    return result.json()


def type_role():
    role = MasterModel(host=config['HOST'], token=token()['token'])

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'REGIN'
    schema['description'] = 'Register Berkas Masuk'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'REGOUT'
    schema['description'] = 'Register Berkas Keluar'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'SURVEY'
    schema['description'] = 'Petugas Ukur'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'DRAWING'
    schema['description'] = 'Petugas Penggambaran dan Pemetaan'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'MANAGER'
    schema['description'] = 'Koreksi dan Validasi Berkas dan Document'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

    schema = role.schema
    schema['_id'] = uuid.uuid4().__str__()
    schema['type'] = "typerole"
    schema['code'] = 'ADMINISTRATOR'
    schema['description'] = 'Pengelola Aplikasi dan Data'
    schema['actived'] = True
    count = role.count(type=schema['type'], code=schema['code'])
    if count.json()['result'] == 0:
        print("-> Insert {}: {}".format(schema['description'], role.add(master=schema).json()['result']))

def add_office():
    office = OfficeModel(host=config['HOST'], token=token()['token'])
    offices = office.all_kkp()
    if offices.status_code == 200:
        for o in offices.json()['result']:
            if o['code'] == '2205':
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

            # elif o['code'] == '1211':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'],kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

            # elif o['code'] == '1205':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'], kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

            # elif o['code'] == '1203':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'], kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

            # elif o['code'] == '1205':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'], kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

            # elif o['code'] == '1208':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'], kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)

            # elif o['code'] == '1209':
            #     print("{} - {}".format(o['code'], o['name']))

            #     schema_office = office.kkpTooffice(officeid=o['officeid'], kkp=office.kkp(officeid=o['officeid']).json()['result'], actived=True)
            #     office.add(office=schema_office)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="REGISTER").status_code == 400:
            #         register = office.counter_schema
            #         register['key'] = 'REGISTER'
            #         register['value'] = 0
            #         register['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=register)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="DOCUMENT").status_code == 400:
            #         document = office.counter_schema
            #         document['key'] = 'DOCUMENT'
            #         document['value'] = 0
            #         document['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=document)

            #     if office.counter(typeid="_id", officeid=o['officeid'], counterid="TOOL").status_code == 400:
            #         tools = office.counter_schema
            #         tools['key'] = 'TOOL'
            #         tools['value'] = 0
            #         tools['actived'] = True
            #         office.add_counter(typeid="_id", officeid=o['officeid'], counter=tools)


    else:
        print('Error: Response not found.')



def add_user():
    # schema = {}
    # user = UserModel(officeid="61352FE6680B5E7BE040A8C01001254C", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="herup3").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "herup3"
    # schema['officeid'] = "61352FE6680B5E7BE040A8C01001254C"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="61352FE6680B5E7BE040A8C01001254C", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="majidp3").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "majidp3"
    # schema['officeid'] = "61352FE6680B5E7BE040A8C01001254C"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="61352FE6680B5E7BE040A8C01001254C", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="rakawidiyatamajr").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "rakawidiyatamajr"
    # schema['officeid'] = "61352FE6680B5E7BE040A8C01001254C"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())


    schema = {}
    user = UserModel(officeid="d8af2d0372b84f6fb33a97847b94cacd", host=config['HOST'], token=token()['token'])
    data = user.pegawai(username="hayudeny").json()['result']
    schema['_id'] = data['userid']
    schema['username'] = "hayudeny"
    schema['officeid'] = "d8af2d0372b84f6fb33a97847b94cacd"
    schema['pegawaiid'] = data['pegawaiid']
    schema['nama'] = data['nama']
    schema['role'] = []
    schema['actived'] = True
    print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="d8af2d0372b84f6fb33a97847b94cacd", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="s4rdh0n0").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "s4rdh0n0"
    # schema['officeid'] = "d8af2d0372b84f6fb33a97847b94cacd"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="a75dfe5e044b454b836a8476dbbbaedd", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="Tata1").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "Tata1"
    # schema['officeid'] = "a75dfe5e044b454b836a8476dbbbaedd"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="c166096f234b4020ae6c5bad24e99419", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="Dicky2000").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "Dicky2000"
    # schema['officeid'] = "c166096f234b4020ae6c5bad24e99419"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="a75dfe5e044b454b836a8476dbbbaedd", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="Tata1").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "Tata1"
    # schema['officeid'] = "c166096f234b4020ae6c5bad24e99419"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="2a3c90a9fa9b4a06a678d512fe6d2847", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="3525100202980001").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "3525100202980001"
    # schema['officeid'] = "2a3c90a9fa9b4a06a678d512fe6d2847"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="2a3c90a9fa9b4a06a678d512fe6d2847", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="3525102411970001").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "3525102411970001"
    # schema['officeid'] = "2a3c90a9fa9b4a06a678d512fe6d2847"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())


    # schema = {}
    # user = UserModel(officeid="2a3c90a9fa9b4a06a678d512fe6d2847", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="3515080912950001").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "3515080912950001"
    # schema['officeid'] = "2a3c90a9fa9b4a06a678d512fe6d2847"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())


    # schema = {}
    # user = UserModel(officeid="4514cb0fb65a4a70b15e47f5bf015386", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="mitrakerjakotaprob8").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "mitrakerjakotaprob8"
    # schema['officeid'] = "4514cb0fb65a4a70b15e47f5bf015386"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

    # schema = {}
    # user = UserModel(officeid="4514cb0fb65a4a70b15e47f5bf015386", host=config['HOST'], token=token()['token'])
    # data = user.pegawai(username="mitrakerjakotaprob9").json()['result']
    # schema['_id'] = data['userid']
    # schema['username'] = "mitrakerjakotaprob9"
    # schema['officeid'] = "4514cb0fb65a4a70b15e47f5bf015386"
    # schema['pegawaiid'] = data['pegawaiid']
    # schema['nama'] = data['nama']
    # schema['role'] = []
    # schema['actived'] = True
    # print(user.add(user=schema).json())

if __name__ == "__main__":
    # add_office()
    add_user()
    # type_role()
