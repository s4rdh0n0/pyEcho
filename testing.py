import requests

# Tornado
import tornado.gen

# Model
from model.office import OfficeModel

def auth():
    auth_param = {
        'username': 's4rdh0n0',
        'password': '4231Dodon'
    }
    auth = requests.post('{}/{}/{}'.format("http://localhost:8000", 'auth', 'login'), json=auth_param)
    return auth.json()['token']


def TestingOffice():
    token = auth()
    office = OfficeModel(host="http://localhost:8000", token=token)
    # for o in office.all().json()['result']:
    #     print("Data     : {}".format(o))

    for o in office.all_kkp().json()['result']:
        # print("Data     : {}".format(o))
        child = office.kkp(officeid=o['officeid'])

        conveter = office.kkpTolocal(o['officeid'], child.json()['result'], True)
        print("Data     : {}".format(conveter))

        add = office.add(conveter)
        if add.status_code == 200:
            print(add.json()['result'])

            counter = {'key': 'REGISTER',
                       'value': 0,
                       'createdate': None,
                       'updatedate': None,
                       'actived': True}

            # Add Counter
            office.add_counter(typeid="_id", officeid=o['officeid'], counter=counter)

            # Booking
            counter['value'] = 1
            office.update_counter(typeid="_id", officeid=o['officeid'], counter=counter)
        

    count = office.count().json()['result']
    print(count)

def add_office():
    token = auth()
    office = OfficeModel(host="http://localhost:8000", token=token)
    for o in office.all_kkp().json()['result']:
        kkp = office.kkp(officeid=o['officeid'])
        conveter = office.kkpTolocal(o['officeid'], kkp.json()['result'], True)
        office.add(conveter)

        con_document = {'key': 'DOCUMENT',
                        'value': 0,
                        'createdate': None,
                        'updatedate': None,
                        'actived': True}

        # Add Counter Document
        office.add_counter(typeid="_id", officeid=o['officeid'], counter=con_document)

        con_register = {'key': 'REGISTER',
                        'value': 0,
                        'createdate': None,
                        'updatedate': None,
                        'actived': True}

        # Add Counter Register
        office.add_counter(typeid="_id", officeid=o['officeid'], counter=con_register)

        con_alatukur = {'key': 'ALATUKUR',
                        'value': 0,
                        'createdate': None,
                        'updatedate': None,
                        'actived': True}

        # Add Counter Alat Ukur
        office.add_counter(typeid="_id", officeid=o['officeid'], counter=con_alatukur)

def delete_office():
    token = auth()
    office = OfficeModel(host="http://localhost:8000", token=token)
    for o in office.all().json()['result']:
        print("Data     : {}".format(o))
        office.delete_counter(typeid="_id", officeid=o['_id'], counterid='REGISTER')

def find_counter():
    token = auth()
    office = OfficeModel(host="http://localhost:8000", token=token)
    co = office.counter(typeid="_id", officeid="93975C008CAAEA62E040A8C010017FFF", counterid="REGISTER")
    if co.status_code == 200:
        print(co.json())

find_counter()
