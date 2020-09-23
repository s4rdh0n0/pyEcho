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


class DaftarPegawaiController(BaseController):

    # Page View.
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        response = self.get_user_actived(cookies=self.get_cookies_user())

        # sleep
        tornado.gen.sleep(0.5)

        # load view
        if response.status_code == 200:
            self.page_data['title'] = 'Daftar Pegawai'
            self.page_data['description'] = 'ASN dan PPNPN Actived'
            self.render('page/administrator/daftarpegawai.html', page=self.page_data, useractived=response.json()['result'])

    # Load Data.
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # sleep
        tornado.gen.sleep(0.5)

        # load view
        body = tornado.escape.json_decode(self.request.body)
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.pagination(pegawaiid=body['pegawaiid'], draw=body['draw'], page=body['page'] + 1, limit=body['limit'], start=body['start']))

    # Delete Data
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def delete(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # sleep
        tornado.gen.sleep(0.5)

        body = tornado.escape.json_decode(self.request.body)
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response = user.delete(typeid="_id", userid=body['userid'])
        if response.status_code == 200:
            self.write({'status': response.json()['result']})

    class RoleController(BaseController):
        
        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, userid=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            # sleep
            tornado.gen.sleep(0.5)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            self.write(user.role(typeid="_id",userid=userid))

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def post(self):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            # sleep
            tornado.gen.sleep(0.5)

            # client request
            body = tornado.escape.json_decode(self.request.body)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            master = MasterModel(host=options.apis, token=cookies['token'])
            if user.find_role(typeid="_id", userid=body['userid'], key=body['key']).status_code == 400:

                # convert
                schema = user.role_schema
                schema['key'] = body['key']
                schema['usercreate'] = cookies['userid']
                schema['description'] = master.find(type="typerole", code=body['key']).json()['result']['description']

                response = user.role_add(typeid="_id", userid=body['userid'], role=schema)
                if response.status_code == 200:
                    self.write({"status": response.json(), "msg": "Success"})
            else:
                self.write({"status": False, "msg": "Data sudah ada."})

    class PegawaiController(BaseController):

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, userid=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            tornado.gen.sleep(0.5)
            
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            master = MasterModel(host=options.apis, token=cookies['token'])
            
            ruser = user.find(typeid="_id", userid=userid)
            tornado.gen.sleep(0.5)
            rtype = master.get_master(type="typerole")

            if ruser.status_code == 200 and rtype.status_code == 200:
                self.render('node/detailpegawai.html', user=ruser.json()['result'], typeregister=rtype.json()['result'])

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def post(self, userid=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            # sleep
            tornado.gen.sleep(0.5)

            # client request
            body = tornado.escape.json_decode(self.request.body)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            master = MasterModel(host=options.apis, token=cookies['token'])
            if user.find_role(typeid="_id", userid=userid, key=body['key']).status_code == 400:

                # convert
                schema = user.role_schema
                schema['key'] = body['key']
                schema['usercreate'] = cookies['userid']
                schema['description'] = master.find(type="typerole", code=body['key']).json()['result']['description']

                response = user.role_add(typeid="_id", userid=userid, role=schema)
                if response.status_code == 200:
                    self.write({"status": response.json(), "msg": "Success"})
            else:
                self.write({"status": False, "msg": "Data sudah ada."})

class ActivationUserController (BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        # sleep
        tornado.gen.sleep(0.5)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response_entity = user.entity(username=body['username'])
        # print(response_entity.json())
        if response_entity.status_code == 200:
            if response_entity.json()['result']['profile']['profilepegawai'] == None:
                self.write({'status': False, 'type': 'warning', 'username': None, 'msg': 'Username tidak terdaftar pada database http://kkp.atrbpn.go.id/ Kantah Trenggalek'})
            else:
                self.write({'status': True, 'type': 'success', 'username': body['username']})
        else:
            self.write({'status': False, 'type': 'danger', 'username': None, 'msg': 'Error response http://kkp.atrbpn.go.id/'})


    class InformasiPegawaiController(BaseController):

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, username=""):            
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()
            
            tornado.gen.sleep(0.5)
            
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            response_count = user.count(typeid="username", userid=username)
            tornado.gen.sleep(0.5)
            response_pegawai = user.pegawai(username=username)

            if response_pegawai.status_code == 200 & response_count.status_code == 200:
                self.render('node/detailuser.html', pegawai=response_pegawai.json()['result'], username=username, count=response_count.json()['result'])


        @tornado.web.authenticated
        @tornado.gen.coroutine
        def post(self, username=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            tornado.gen.sleep(0.5)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            entity = user.entity(username=username)
            if entity.status_code == 200:
                schema = user.schema
                schema['_id'] = entity.json()['result']['userid']
                schema['officeid'] = cookies['officeid']
                schema['username'] = username
                schema['pegawaiid'] = entity.json()['result']['pegawaiid']
                schema['nama'] = entity.json()['result']['nama']
                schema['actived'] = True

                tornado.gen.sleep(0.5)

                add = user.add(user=schema)
                if add.status_code == 200:
                    self.write({'status': add.json()['result'], 'type': 'success', 'msg': '{} Actived'.format(schema['nama'])})
                else:
                    self.write({'status': False, 'type': 'danger', 'msg': '{} Gagal Activation'.format(schema['nama'])})
