import requests

# Tornado
import tornado.gen

# Model
from model.user import UserModel
from model.office import OfficeModel
from model.berkas import BerkasModel



config = {
    'HOST': 'http://117.102.75.170:8090'
}


def token():
    user = UserModel(officeid=None, host=config['HOST'], token=None)
    result = user.auth(username="s4rdh0n0", password="YCxa2SJxLXQhFN")
    return result.json()


def main():
    office = OfficeModel(host=config['HOST'], token=token()['token'])
    for o in office.all().json()['result']:
        print(office.kkp(officeid=o['_id']).json()['result'])

if __name__ == "__main__":
    main()
