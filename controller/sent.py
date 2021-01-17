import datetime
from bson import json_util
import json
import uuid


# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options
from tornado import gen

# Controller
from controller.base import BaseController

# Model
from model.region import RegionModel
from model.office import OfficeModel
from model.user import UserModel
from model.berkas import BerkasModel
from model.region import RegionModel
from model.master import MasterModel
from model.register import RegisterModel

class SentController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            if UserModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="users"), service=options.service).find_role(userid=useractived['_id'], role="REGISTER") != None and useractived['actived']:
                self.page_data['title'] = 'Sent'
                self.page_data['description'] = 'Daftar Berkas Terkirim'
                self.render('page/register/sent.html', page=self.page_data, useractived=useractived)

            else:
                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
        else:
            self.redirect("/logout")

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            cookies = self.get_cookies_user()
            body = tornado.escape.json_decode(self.request.body)

            list_response = []
            count_reponse = 0

            inbox = RegisterModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="register"), service=None)
            if body['nomor']  == "" and body['tahun'] == "":
                count_reponse = inbox.count(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] })
                list_response  = inbox.pagination(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid']}, page_size=body['limit'], page_num=body['page'] + 1)
            elif body['nomor']  != "" and body['tahun'] == "":
                count_reponse = inbox.count(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] ,"nomorberkas": body['nomor'] })
                list_response  = inbox.pagination(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] ,"nomorberkas": body['nomor'] }, page_size=body['limit'], page_num=body['page'] + 1)               
            elif body['nomor']  == "" and body['tahun']  != "":
                count_reponse = inbox.count(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] , "tahunberkas": body['tahun'] })
                list_response  = inbox.pagination(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] ,"tahunberkas": body['tahun'] }, page_size=body['limit'], page_num=body['page'] + 1)
            else:
                count_reponse = inbox.count(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] ,"nomorberkas": body['nomor'] ,"tahunberkas": body['tahun'] })
                list_response  = inbox.pagination(filter={"officeid": cookies['officeid'] ,"sender": cookies['userid'] ,"nomorberkas": body['nomor'] ,"tahunberkas": body['tahun'] }, page_size=body['limit'], page_num=body['page'] + 1)

            result = []
            for x in list_response:
                x['berkas'] = BerkasModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="berkas"), service=None).get(filter={'_id': x['berkasid']})
                result.append(x)

            self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(result, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
        else:
            self.redirect("/logout")

