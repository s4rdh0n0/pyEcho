import datetime
import requests

# Tornado Framework
import tornado.web
import tornado.gen
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.user import UserModel
from model.master import MasterModel


class DaftarPegawaiController(BaseController):

    @tornado.web.authenticated
    def get(self):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        try:
            response = self.get_user_actived(cookies=self.get_cookies_user())
            if  response.status_code == 200:
                self.page_data['title'] = 'Daftar Pegawai'
                self.page_data['description'] = 'Pegawai Actived/Non Actived'
                self.render('administrator/daftarpegawai.html', page=self.page_data, useractived=response.json()['result'])
        except Exception as e:
        	self.write(e)


    @tornado.web.authenticated
    def post(self):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        body = tornado.escape.json_decode(self.request.body)
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.get_all(pegawaiid=body['pegawaiid'], draw=body['draw'], page=body['page'] + 1, limit=body['limit'], start=body['start']))


    @tornado.web.authenticated
    def put(self):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        body = tornado.escape.json_decode(self.request.body)
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        rkkp_user = user.get_user(db="kkp", type="username", id=body["username"])
        if rkkp_user.status_code == 200:
            if rkkp_user.json()['result']['profile']['profilepegawai'] != None:
                if user.get_user(db="local", type="username", id=body["username"]).status_code == 200:
                    self.write({'status': False, 'data': None, 'msg': 'Pegawai sudah terdaftar pada database.'})
                else:
                    self.write({'status': True, 'data': rkkp_user.json(), 'msg': None})
            else:
                self.write({'status': False, 'data': None, 'msg': 'Pegawai tidak terdaftar pada database kkp.atrbpn.go.id'})
        else:
            self.write({'status': False, 'data': None, 'msg': 'Server not response'})


    class PegawaiController(BaseController):

        @tornado.web.authenticated
        @tornado.gen.coroutine
        def get(self, userid=""):
            # NOTE: refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()
            
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            master = MasterModel(type='typeregister', host=options.apis, token=cookies['token'])

            ruser = user.get_user(db="local", type="_id", id=userid)
            tornado.gen.sleep(0.5)
            rmaster = master.get_master()

            if ruser.status_code == 200 and rmaster.status_code == 200:
                self.render('administrator/detailpegawai.html', user=ruser.json()['result'], typeregister=rmaster.json()['result'])


        @tornado.web.authenticated
        def post(self):
            # NOTE: refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            body = tornado.escape.json_decode(self.request.body)
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            rschema = user.get_schema()
            rkkp_user = user.get_user("kkp", "username", body['username'])
            if rkkp_user.status_code == 200 and rschema.status_code == 200:
                pschema  = rschema.json()['result']
                pkkp_user = rkkp_user.json()['result']
                
                # converter:
                pschema['_id'] = pkkp_user['userid']
                pschema['officeid'] = cookies['officeid']
                pschema['username'] = body['username']
                pschema['pegawaiid'] = pkkp_user['pegawaiid']
                pschema['nama'] = pkkp_user['nama']
                pschema['image'] = pkkp_user['photo']
                pschema['phone'] = pkkp_user['phone']
                pschema['actived'] = True

                if user.add_user(data=pschema).status_code == 200:
                    self.write({'status': True, 'type': 'success','msg': 'Pegawai berhasil disimpan.'})
                else:
                    self.write({'sttaus': False, 'type': 'warning','msg': 'Pegawai gagal disimpan.'})

    class RoleController(BaseController):

        @tornado.web.authenticated
        def post(self):
            # NOTE: refresh cookies data
            self.refresh_cookies(cookies=self.get_cookies_user())
            cookies = self.get_cookies_user()

            body = tornado.escape.json_decode(self.request.body)
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            response = user.role.get_role(userid=body['userid'])
            if response.status_code == 200:
                if response.json()['result'] != None:
                    self.write({'draw': 0, 'data': response.json()['result'], 'recordsTotal': len(response.json()['result']), 'recordsFiltered': len(response.json()['result'])})
                else:
                    self.write({'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0})
            else:
                self.write({'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0})
