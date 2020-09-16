import requests
import datetime

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
            self.page_data['description'] = 'Pegawai Actived/Non Actived'
            self.render('page/administrator/daftarpegawai.html', page=self.page_data, useractived=response.json()['result'])

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

        # load pagination
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.pagination(pegawaiid=body['pegawaiid'], draw=body['draw'], page=body['page'] + 1, limit=body['limit'], start=body['start']))
        
        
    class KKPPegawaiController(BaseController):

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, username=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            # sleep
            tornado.gen.sleep(0.5)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            response_kkp_user = user.kkp(username=username)
            if response_kkp_user.status_code == 200:
                if response_kkp_user.json()['result']['profile']['profilepegawai'] != None:
                    if user.find(typeid="username", userid=username).status_code == 200:
                        self.write({'status': False, 'data': None, 'msg': 'Pegawai sudah terdaftar pada database.'})
                    else:
                        self.write({'status': True, 'data': response_kkp_user.json(), 'msg': None})
                else:
                    self.write({'status': False, 'data': None, 'msg': 'Pegawai tidak terdaftar pada database kkp.atrbpn.go.id'})
            else:
                self.write({'status': False, 'data': None, 'msg': 'Server not response'})

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def post(self, username=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            # sleep
            tornado.gen.sleep(0.5)

            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            rschema = user.schema
            rkkp_user = user.kkp(username=username)
            
            if rkkp_user.status_code == 200:
                pkkp_user = rkkp_user.json()['result']
                
                # converter
                rschema['_id'] = pkkp_user['userid']
                rschema['officeid'] = cookies['officeid']
                rschema['username'] = username
                rschema['pegawaiid'] = pkkp_user['pegawaiid']
                rschema['nama'] = pkkp_user['nama']
                rschema['image'] = pkkp_user['photo']
                rschema['phone'] = pkkp_user['phone']
                rschema['actived'] = True

                if user.add(user=rschema).status_code == 200:
                    self.write({'status': True, 'type': 'success','msg': 'Pegawai berhasil disimpan.'})
                else:
                    self.write({'sttaus': False, 'type': 'warning','msg': 'Pegawai gagal disimpan.'})

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
            schema = user.role_schema

            # convert
            schema['code'] = body['code']
            schema['createdate'] = datetime.datetime.now()
            schema['usercreate'] = cookies['userid']
            schema['description'] = body['description']

            response = user.role_add(typeid="_id", userid=body['userid'], role=schema)
            if response.status_code == 200:
                self.write(response.json())

    class PegawaiController(BaseController):

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, userid=""):
            # refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            tornado.gen.sleep(0.5)
            
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            master = MasterModel(type='typeregister', host=options.apis, token=cookies['token'])
            
            ruser = user.find(typeid="_id", userid=userid)
            tornado.gen.sleep(0.5)
            rtype = master.get_master()

            if ruser.status_code == 200 and rtype.status_code == 200:
                self.render('node/detailpegawai.html', user=ruser.json()['result'], typeregister=rtype.json()['result'])
