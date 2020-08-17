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
            # NOTE: header JWT
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}

            # NOTE: Count the number of records
            paramRecords = 'officeid={}'.format(cookies['officeid'])
            records = requests.get('{}/offices/users/count?{}'.format(options.apis, paramRecords), headers=dheader)

            # NOTE: Load entire user data
            paramUsers = 'officeid={}&limit={}&page={}'.format(cookies['officeid'], body['limit'], body['page'] + 1)
            users = requests.get('{}/{}{}'.format(options.apis, 'offices/users?', paramUsers), headers=dheader)
            if users.status_code == 200 and records.status_code == 200:
                self.write({'status': True, 'draw': body['draw'], 'data': users.json()['result'], 'recordsTotal': records.json()['result'], 'recordsFiltered': records.json()['result']})
            else:
                pass
        except Exception as e:
            self.write({'status': False, 'msg': e})

    @tornado.web.authenticated
    def put(self, username=""):
        cookies = self.get_cookies_user()
        self.refresh_cookies(cookies=cookies)
        try:
            # NOTE: header JWT
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}

            # NOTE: load kkp data
            paramKKP = 'officeid={}&username={}'.format(cookies['officeid'], username)
            responKKP = requests.get('{}/{}{}'.format(options.apis, 'offices/users/kkp?', paramKKP), headers=dheader)
            
            if responKKP.status_code == 200:
                # NOTE: load db data
                paramDB = 'id={}&type=username'.format(username)
                responDB = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?', paramDB), headers=dheader)
                
                if responDB.status_code == 200:
                    self.write({'status': False, 'data': None, 'msg': 'Username sudah terdaftar pada aplikasi ini.'})
                else:
                    if responKKP.json()['result']['profile']['profilepegawai'] != None:
                        self.write({'status': True, 'data':responKKP.json()})
                    else:
                        self.write({'status': False, 'data': None, 'msg': 'Username sudah tidak terdaftar database kkp.'})


        except Exception as e:
       	    self.write(e)
        
