import requests

# Tornado Framework
import tornado.web
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController



class AddPegawaiController(BaseController):

    @tornado.web.authenticated
    def post(self):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())

        # NOTE: respon body
        body = tornado.escape.json_decode(self.request.body)
        try:
            # NOTE: header JWT
            cookies = self.get_cookies_user()
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}        
            djson = {"officeid": body["officeid"],
                     "username": body["username"]}
            addUser = requests.post('{}/{}'.format(options.apis, 'offices/users/add'), json=djson, headers=dheader)
            if addUser.status_code == 200:
                self.write({'status': True, 'data': addUser.json(), 'type':'success', 'msg': 'Data pegawai berhasil tersimpan.'})
            else:
                self.write({'status': True, 'data': None, 'type':'warning', 'msg': addUser.json()['msg']})
        
        except Exception as e:
            self.write({'status': False, 'msg': e})


class DaftarPegawaiController(BaseController):

    @tornado.web.authenticated
    def get(self):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        try:
            cookies = self.get_cookies_user()
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

        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        try:
            # NOTE: header JWT
            cookies = self.get_cookies_user()
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}

            # NOTE: Count the number of records
            paramRecords = 'officeid={}'.format(cookies['officeid'])
            records = requests.get('{}/offices/users/count?{}'.format(options.apis, paramRecords), headers=dheader)

            # NOTE: Load entire user data
            paramUsers = 'officeid={}&pegawaiid={}&limit={}&page={}'.format(cookies['officeid'], body['pegawaiid'], body['limit'], body['page'] + 1)
            users = requests.get('{}/{}{}'.format(options.apis, 'offices/users?', paramUsers), headers=dheader)
            if users.status_code == 200 and records.status_code == 200:
                if users.json()['result'] != None:
                    self.write({'status': True, 'draw': body['draw'], 'data': users.json()['result'], 'recordsTotal': records.json()['result'], 'recordsFiltered': records.json()['result']})
                else:
                    self.write({'status': True, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0})
            else:
                pass
        except Exception as e:
            self.write({'status': False, 'msg': e})

    @tornado.web.authenticated
    def put(self, username=""):
        # NOTE: refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        try:
            # NOTE: header JWT
            cookies = self.get_cookies_user()
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}

            # NOTE: load kkp user
            paramKKP = 'officeid={}&id={}&db=kkp'.format(cookies['officeid'], username)
            responKKP = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?', paramKKP), headers=dheader)
            
            if responKKP.status_code == 200:

                # NOTE: load db user
                paramDB = 'id={}&type=username&db=local'.format(username)
                responDB = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?', paramDB), headers=dheader)
                
                if responDB.status_code == 200:
                    self.write({'status': False, 'data': None, 'msg': 'Pegawai sudah terdaftar pada aplikasi ini.'})
                else:
                    if responKKP.json()['result']['profile']['profilepegawai'] != None:
                        self.write({'status': True, 'data':responKKP.json()})
                    else:
                        self.write({'status': False, 'data': None, 'msg': 'Pegawai tidak terdaftar pada database kkp.'})


        except Exception as e:
       	    self.write(e)
