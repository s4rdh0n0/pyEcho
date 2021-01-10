import requests
import datetime
from bson import json_util
import json
import uuid

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
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            collection = self.CONNECTION.collection(database="registerdb", name="users")
            if UserModel(collection=collection, service=options.service).find_role(userid=useractived['_id'], role="ADMINISTRATOR") != None and useractived['actived']:

                self.page_data['description'] = 'ASN dan PPNPN Actived'
                self.page_data['title'] = 'Daftar Pegawai'
                self.render('page/administrator/daftarpegawai.html', page=self.page_data, useractived=useractived)
                    
            else:
                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
        else:
            self.redirect("/logout")

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user = UserModel(collection=self.CONNECTION.collection(database="registerdb", name="users"), service=options.service)
        list_response = []
        count_reponse = 0

        if body['pegawaiid'] != "":
            count_reponse = user.count(filter={"$and": [{'officeid': cookies['officeid']} ,{"pegawaiid": str(body['pegawaiid'])}]})
            list_response = user.pagination(filter={"$and": [{'officeid': cookies['officeid']}, {"pegawaiid": str(body['pegawaiid'])}]}, page_size=body['limit'], page_num=body['page'] + 1)

        else:
            count_reponse = user.count(filter={"officeid": cookies['officeid']})
            list_response = user.pagination(filter={'officeid': cookies['officeid']}, page_size=body['limit'], page_num=body['page'] + 1)
            
        
        self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def put(self):
        # client request
        cookies = self.get_cookies_user()
        body = tornado.escape.json_decode(self.request.body)
        collection = self.CONNECTION.collection(database="registerdb", name="users")

        user = UserModel(collection=collection, service=options.service)
        responseUser = user.get(filter={"_id": body['userid']})

        if responseUser != None:
            userSchema = responseUser
            if userSchema['actived']:
                userSchema['userupdate'] = cookies['userid']
                userSchema['updatedate'] = datetime.datetime.now()
                userSchema['actived'] = False
            else:
                userSchema['userupdate'] = cookies['userid']
                userSchema['updatedate'] = datetime.datetime.now()
                userSchema['actived'] = True

            user.update(filter={"_id": body['userid']}, schema=userSchema)
            self.write({'status': True})
        else:
            self.write({'status': False})


class PegawaiController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, username=""):
        cookies = self.get_cookies_user()

        collection = self.CONNECTION.collection(database="registerdb", name="users")
        user = UserModel(collection=collection, service=options.service)
        response_count = user.count(filter={"username": username})
        response_pegawai = user.kkp(officeid=cookies['officeid'],username=username)
        if response_pegawai.status_code == 200:
            self.render('node/detailuser.html', pegawai=response_pegawai.json()['result'], username=username, count=response_count)
        else:
	        self.redirect("/logout")

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def put(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)
        collection = self.CONNECTION.collection(database="registerdb", name="users")
        user = UserModel(collection=collection, service=options.service)
        response_entity = user.kkp(officeid=cookies['officeid'], username=body['username'])
        if response_entity.status_code == 200:
            if response_entity.json()['result']['profile']['profilepegawai'] == None:
                self.write({'status': False, 'type': 'warning', 'username': None, 'msg': 'Username tidak terdaftar pada database http://kkp.atrbpn.go.id/ Kantah Trenggalek'})
            else:
                self.write({'status': True, 'type': 'info', 'username': body['username']})
        else:
            self.write({'status': False, 'type': 'warning', 'username': None, 'msg': 'Error response http://kkp.atrbpn.go.id/'})

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)
        collection = self.CONNECTION.collection(database="registerdb", name="users")
        user = UserModel(collection=collection, service=options.service)
        count_reponse = user.count(filter={"_id": body['userid']})
        if count_reponse == 0:
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
            schema['createdate'] = datetime.datetime.now()
            schema['actived'] = True

            user.add(schema=schema)
            self.write({'status': True, 'type': 'info', 'msg': '{} Actived'.format(schema['nama'])})

class RoleController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, userid=""):
        cookies = self.get_cookies_user()

        user_collection = self.CONNECTION.collection(database="registerdb", name="users")
        master_collection = self.CONNECTION.collection(database="registerdb", name="master")

        ruser = UserModel(collection=user_collection, service=options.service).get(filter={"_id": userid})
        rtype = MasterModel(collection=master_collection, service=options.service).select(filter={"type": "ROLE"})
        self.render('node/detailrole.html', user=ruser, typeregister=rtype)


    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        collection = self.CONNECTION.collection(database="registerdb", name="users")
        user = UserModel(collection=collection, service=options.service).get(filter={"_id": body['userid']})
        self.write({'status': True, 'draw': 0, 'data': json.dumps(user['role'], default=json_util.default), 'recordsTotal': len(user['role']), 'recordsFiltered': len(user['role'])})

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def put(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user_collection = self.CONNECTION.collection(database="registerdb", name="users")
        master_collection = self.CONNECTION.collection(database="registerdb", name="master")
        master = MasterModel(collection=master_collection, service=options.service).get(filter={"type": "ROLE", "code": body['key']})

        if UserModel(collection=user_collection, service=options.service).find_role(userid=body['userid'], role=master['code']) == None:

            schema_role = UserModel(collection=user_collection, service=options.service).schema_role
            schema_role['key'] = master['code']
            schema_role['description'] = master['description']
            schema_role['startdate'] = datetime.datetime.now()
            UserModel(collection=user_collection, service=options.service).add_role(userid=body['userid'], schema=schema_role)

            schema_user = UserModel(collection=user_collection, service=options.service).get(filter={"_id": body['userid']})
            schema_user['userupdate'] = cookies['userid']
            schema_user['updatedate'] = datetime.datetime.now()

            UserModel(collection=user_collection, service=options.service).update(filter={"_id": body['userid']}, schema=schema_user)
            self.write({"status": True, "msg": None})
        else:
            self.write({"status": False, "msg": "Data sudah ada."})

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def delete(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        user_collection = self.CONNECTION.collection(database="registerdb", name="users")
        user = UserModel(collection=user_collection, service=options.service).delete_role(userid=body['userid'], role=body['key'])
        self.write({'status': True})
