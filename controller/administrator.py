import requests

# Tornado Framework
import tornado.web
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.user import UserModel



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
        self.refresh_cookies(cookies=self.get_cookies_user())
        body = tornado.escape.json_decode(self.request.body)
        try:
            cookies = self.get_cookies_user()
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            self.write(user.get_all(pegawaiid=body['pegawaiid'], draw=body['draw'], page=body['page'] + 1, limit=body['limit'], start=body['start']))
        except Exception as e:
            self.write({'status': False, 'msg': e})


    @tornado.web.authenticated
    def put(self, username=""):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        try:
            cookies = self.get_cookies_user()
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])

            user_kkp = user.get_user(db="kkp", type="username", id=username)
            if user_kkp.status_code == 200:
                if user_kkp.json()['result']['profile']['profilepegawai'] != None:
                    user_db = user.get_user(db="local", type="username", id=username)
                    if user_db.status_code == 200:
                        self.write({'status': False, 'data': None, 'msg': 'Pegawai sudah terdaftar pada database.'})
                    else:
                        self.write({'status': True, 'data': user_kkp.json(), 'msg': None})
                else:
                    self.write({'status': False, 'data': None, 'msg': 'Pegawai tidak terdaftar pada database kkp.atrbpn.go.id'})
            else:
                self.write({'status': False, 'data': None, 'msg': 'Server not response'})

        except Exception as e:
       	    self.write(e)


    class PegawaiController(BaseController):

        @tornado.web.authenticated
        def get(self, userid=""):
            self.refresh_cookies(cookies=self.get_cookies_user())

            cookies = self.get_cookies_user()
            user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
            response = user.get_user(db="local", type="_id", id=userid)
            if response.status_code == 200:
                self.render('administrator/detailpegawai.html', user=response.json()['result'])



        @tornado.web.authenticated
        def post(self):
            self.refresh_cookies(cookies=self.get_cookies_user())
            body = tornado.escape.json_decode(self.request.body)
            try:
                cookies = self.get_cookies_user()
                user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
                self.write(user.set_user(username=body['username']))

            except Exception as e:
                self.write({'status': False, 'msg': e})

        @tornado.web.authenticated
        def put(self):
            self.refresh_cookies(cookies=self.get_cookies_user())


        @tornado.web.authenticated
        def delete(self):
            pass