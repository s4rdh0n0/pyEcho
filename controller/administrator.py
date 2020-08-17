import requests

# Tornado Framework
import tornado.web
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

class DaftarPegawaiController(BaseController):

    @tornado.web.authenticated
    def get(self):
        cookies = self.get_cookies_user()
        self.refresh_cookies(cookies=cookies)
        try:
            respon = self.get_user_actived(cookies=cookies)
            if  respon.status_code == 200:
                self.page_data['title'] = 'Daftar Pegawai'
                self.page_data['description'] = 'Employeed Actived/Non Actived'
                self.render('administrator/daftarpegawai.html', page=self.page_data, useractived=respon.json()['result'])
        except Exception as e:
        	self.write(e)

    @tornado.web.authenticated
    def post(self):
        # NOTE: respon body
        body = tornado.escape.json_decode(self.request.body)

        # NOTE: load cookies data
        cookies = self.get_cookies_user()
        self.refresh_cookies(cookies=cookies)
        try:
            # NOTE: load users
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
            param = 'officeid={}&limit={}&page={}'.format(cookies['officeid'], body['limit'], 1)
            users = requests.get('{}/{}{}'.format(options.apis, 'offices/users?', param), headers=dheader)
            if users.status_code == 200:
                self.write({'status': True, 'draw': body['draw'], 'data': users.json()['result'], 'recordsTotal': body['limit'], 'recordsFiltered': body['limit']})
            else:
                pass
        except Exception as e:
            self.write(e)
        
