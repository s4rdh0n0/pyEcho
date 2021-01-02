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

        if useractived.status_code == 200:
            role = self.get_user_role(cookies=self.get_cookies_user(), key="ADMINISTRATOR")
            if role.status_code == 200:

                self.page_data['description'] = 'ASN dan PPNPN Actived'
                self.page_data['title'] = 'Daftar Pegawai'
                self.render('page/administrator/daftarpegawai.html', page=self.page_data, useractived=useractived.json()['result'])
                    
            else:

                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived.json()['result'])
        else:
            self.redirect("/login")

    # Load Data.
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        count_reponse = user.count(typeid="pegawaiid", userid=body['pegawaiid'])
        if count_reponse.status_code == 200:
            list_response = user.pagination(pegawaiid=body['pegawaiid'], page=body['page'] + 1, limit=body['limit'])
            if list_response.status_code == 200:
                data = list_response.json()['result']
                count = count_reponse.json()['result']
                if data == None:
                    data = []
                    count = 0 

                self.write({'status': True, 'draw': body['draw'], 'data': data, 'recordsTotal': count, 'recordsFiltered': count})
            else:
                self.write({'status': False, 'draw':0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0 })
        else:
            self.write({'status': False, 'draw':0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0 })

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def put(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        responseUser = user.find(typeid="_id", userid=body['userid'])

        if responseUser.status_code == 200:
            userSchema = responseUser.json()['result']
            if userSchema['actived']:
                userSchema['userupdate'] = cookies['userid']
                userSchema['actived'] = False
                user.update(user=userSchema)
            else:
                userSchema['userupdate'] = cookies['userid']
                userSchema['actived'] = True
                user.update(user=userSchema)

            self.write({'status': True})
        else:
            self.write({'status': False})


class PegawaiController(BaseController):

    @tornado.web.authenticated
    def get(self, username=""):
        # refresh cookies data
        # self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()
        
        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response_count = user.count(typeid="username", userid=username)
        response_pegawai = user.pegawai(username=username)
        if response_pegawai.status_code == 200 & response_count.status_code == 200:
            self.render('node/detailuser.html', pegawai=response_pegawai.json()['result'], username=username, count=response_count.json()['result'])
        else:
	        self.redirect("/login")

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def put(self):
        # refresh cookies data
        # self.refresh_cookies(cookies=self.get_cookies_user())
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
    @tornado.gen.coroutine
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        count_reponse = user.count(typeid="_id", userid=body['userid'])
        schema = user.schema

        schema['_id'] = body['userid']
        schema['officeid'] = cookies['officeid']
        schema['username'] = body['username']
        schema['password'] = body['password']
        schema['pegawaiid'] = body['pegawaiid']
        schema['nama'] = body['nama']
        schema['phone'] = body['phone']
        schema['email'] = body['email']
        schema['usercreate'] = cookies['userid']
        schema['actived'] = True

        add = user.add(user=schema)
        if add.status_code == 200:
            self.write({'status': add.json()['result'], 'type': 'success', 'msg': '{} Actived'.format(schema['nama'])})
        else:
            self.write({'status': False, 'type': 'danger', 'msg': '{} Gagal Activation'.format(schema['nama'])})


class RoleController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
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
    @tornado.gen.coroutine
    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        self.write(user.role(typeid="_id", userid=body['userid']))

    @tornado.web.authenticated
    @tornado.gen.coroutine
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
            schema['description'] = role.json()['result']['description']

            response = user.role_add(typeid="_id", userid=body['userid'], role=schema)
            if response.status_code == 200:
                self.write({"status": response.json(), "data": schema})
            else:
                self.write({"status": False, "msg": "Internal server error."})
        else:
            self.write({"status": False, "msg": "Data sudah ada."})

    @tornado.web.authenticated
    @tornado.gen.coroutine
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
