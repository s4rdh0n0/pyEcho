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


@tornado.gen.coroutine
def TestingOffice():
    token = auth()
    office = OfficeModel(host="http://localhost:8000", token=token)
    # for o in office.all().json()['result']:
    #     print("Data     : {}".format(o))

    for o in office.all_kkp().json()['result']:
        # print("Data     : {}".format(o))
        child = office.kkp(officeid=o['officeid'])

        tornado.gen.sleep(0.5)

        conveter = office.kkpTolocal(o['officeid'], child.json()['result'], False)
        print("Data     : {}".format(conveter))


        tornado.gen.sleep(0.5)

        add = office.add(conveter)
        print(add.json()['result'])
        

    count = office.count().json()['result']
    print(count)

    schema = office.schema().json()['result']
    print(schema)


TestingOffice()
