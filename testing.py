import datetime

from model.base import ConnectionModel
from model.office import OfficeModel

collection = ConnectionModel(username="1228_adminregister", password="1228trenggalek", server="localhost", port="27017").collection(database="registerdb", name="offices")
o = OfficeModel(collection=collection, service="http://localhost:8000")


# print(o.kkp().json()['result'])
for a in o.kkp().json()['result']:
    # print(o.count(filter={"_id": a['officeid']}))
    x = o.find_kkp(officeid=a['officeid']).json()
    if o.count(filter={"_id": a['officeid']}) > 0:
        o.delete_counter(officeid=a['officeid'], counter="REGISTERBERKAS")
        # print(o.find_kkp(officeid=a['officeid']).json())
    else:
        schema = {'_id': a['officeid'],
                  'code': x['result']['code'],
                  'officetypeid': x['result']['officetypeid'],
                  'parent': x['result']['parent'],
                  'nama': x['result']['name'],
                  'kota': x['result']['city'],
                  'alamat': x['result']['address'],
                  'phone': x['result']['phone'],
                  'email': x['result']['email'],
                  'fax': x['result']['fax'],
                  'counter': [],
                  'actived': False}

        print(o.add(schema=schema))

        counter = {'key': "REGISTERBERKAS",
                   'value': 1,
                   'startdate': datetime.datetime.now()}
        o.add_counter(filter={"_id": a['officeid']}, schema=counter)
        counter = {'key': "UPLOADFILE",
                   'value': 1,
                   'startdate': datetime.datetime.now()}
        o.add_counter(filter={"_id": a['officeid']}, schema=counter)

        

# for p in range(10):
#     print(o.pagination(page_size=20, page_num=p+1))
#     print("")


# print(o.get(filter={"_id": "d8af2d0372b84f6fb33a97847b94cacd"}))
