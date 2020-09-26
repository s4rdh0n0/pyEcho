import requests

# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.user import UserModel
from model.master import MasterModel


class DaftarPegawaiViewController(BaseController):

    @tornado.web.authenticated
    def get(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        useractived = self.get_user_actived(cookies=self.get_cookies_user())

        role = self.get_user_role(cookies=self.get_cookies_user(), key="ADMINISTRATOR")
        if role.status_code == 200:

            # load view
            if useractived.status_code == 200:
                self.page_data['description'] = 'ASN dan PPNPN Actived'
                self.page_data['title'] = 'Daftar Pegawai'
                self.render('page/administrator/daftarpegawai.html', page=self.page_data, useractived=useractived.json()['result'])
            else:
                self.redirect("/login")
        else:
            self.page_data['title'] = '403'
            self.page_data['description'] = 'Access denied'
            self.render("page/error/403.html", page=self.page_data,  useractived=useractived.json()['result'])

    # Load Data.
    @tornado.web.authenticated
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.pagination(pegawaiid=body['pegawaiid'], draw=body['draw'], page=body['page'] + 1, limit=body['limit'], start=body['start']))


class PegawaiController(BaseController):

    @tornado.web.authenticated
    def get(self, username=""):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()
        
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response_count = user.count(typeid="username", userid=username)
        response_pegawai = user.pegawai(username=username)
        if response_pegawai.status_code == 200 & response_count.status_code == 200:
            self.render('node/detailuser.html', pegawai=response_pegawai.json()['result'], username=username, count=response_count.json()['result'])
        else:
	        self.redirect("/login")

    @tornado.web.authenticated
    def put(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response_entity = user.entity(username=body['username'])
        if response_entity.status_code == 200:
            if response_entity.json()['result']['profile']['profilepegawai'] == None:
                self.write({'status': False, 'type': 'warning', 'username': None, 'msg': 'Username tidak terdaftar pada database http://kkp.atrbpn.go.id/ Kantah Trenggalek'})
            else:
                self.write({'status': True, 'type': 'success', 'username': body['username']})
        else:
            self.write({'status': False, 'type': 'danger', 'username': None, 'msg': 'Error response http://kkp.atrbpn.go.id/'})

    @tornado.web.authenticated
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        entity = user.entity(username=body['username'])
        if entity.status_code == 200:
            schema = user.schema
            schema['_id'] = entity.json()['result']['userid']
            schema['officeid'] = cookies['officeid']
            schema['username'] = body['username']
            schema['pegawaiid'] = entity.json()['result']['pegawaiid']
            schema['nama'] = entity.json()['result']['nama']
            schema['actived'] = True

            add = user.add(user=schema)
            if add.status_code == 200:
                self.write({'status': add.json()['result'], 'type': 'success', 'msg': '{} Actived'.format(schema['nama'])})
            else:
                self.write({'status': False, 'type': 'danger', 'msg': '{} Gagal Activation'.format(schema['nama'])})

    def delete(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response = user.delete(typeid="_id", userid=body['userid'])
        if response.status_code == 200:
            self.write({'status': response.json()['result']})
        else:
            self.write({'status': False})


class RoleController(BaseController):

    @tornado.web.authenticated
    def get(self, userid=""):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()   

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        master = MasterModel(host=options.apis, token=cookies['token'])

        ruser = user.find(typeid="_id", userid=userid)
        rtype = master.get_master(type="typerole")  
        if ruser.status_code == 200 and rtype.status_code == 200:
            self.render('node/detailrole.html', user=ruser.json()['result'], typeregister=rtype.json()['result'])
        else:
            self.redirect("/login")

    @tornado.web.authenticated
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.role(typeid="_id", userid=body['userid']))

    @tornado.web.authenticated
    def put(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        master = MasterModel(host=options.apis, token=cookies['token'])
        role = master.find(type="typerole", code=body['key'])
        if user.find_role(typeid="_id", userid=body['userid'], key=body['key']).status_code == 400 and role.status_code == 200:

            # convert
            schema = user.role_schema
            schema['key'] = role.json()['result']['code']
            schema['usercreate'] = cookies['userid']
            schema['description'] = role.json()['result']['description']

            response = user.role_add(typeid="_id", userid=body['userid'], role=schema)
            if response.status_code == 200:
                self.write({"status": response.json(), "data": schema})
            else:
                self.write({"status": False, "msg": "Internal server error."})
        else:
            self.write({"status": False, "msg": "Data sudah ada."})

    @tornado.web.authenticated
    def delete(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response = user.role_delete(userid=body['userid'], key=body['key'])
        if response.status_code == 200:
            self.write({'status': response.json()['result']})
