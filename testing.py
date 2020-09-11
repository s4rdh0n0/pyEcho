import requests

def TestingUser():
    auth_param = {
        'username': 's4rdh0n0',
        'password': '4231Dodon'
    }
    auth = requests.post('{}/{}/{}'.format("http://localhost:8000", 'auth', 'login'), json=auth_param)
    token = auth.json()['token']

    print(token)
    # user = UserModel(officeid="", host="http://localhost:8000", token=token)


TestingUser()
