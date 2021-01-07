import requests
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
from model.inbox import InboxModel



class InboxController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            if UserModel(collection=self.CONNECTION.collection(database="registerdb", name="users"), service=options.service).find_role(userid=useractived['_id'], role="REGISTER") != None and useractived['actived']:
                self.page_data['title'] = 'Inbox'
                self.page_data['description'] = 'Inbox Register Berkas'
                self.render('page/register/inbox.html', page=self.page_data, useractived=useractived)

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

            register = InboxModel(collection=self.CONNECTION.collection(database="registerdb", name="inbox"), service=None)
            if body['nomor']  == "" and body['tahun'] == "":
                count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"status": "PROSES" ,"actived": True})
                list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'],"status": "PROSES" ,"actived": True}, page_size=body['limit'], page_num=body['page'] + 1)
            elif body['nomor']  != "" and body['tahun'] == "":
                count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"nomorberkas": body['nomor'] ,"status": "PROSES" ,"actived": True})
                list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"nomorberkas": body['nomor'] ,"status": "PROSES" ,"actived": True}, page_size=body['limit'], page_num=body['page'] + 1)               
            elif body['nomor']  == "" and body['tahun']  != "":
                count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] , "tahunberkas": body['tahun'] ,"status": "PROSES" ,"actived": True})
                list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"tahunberkas": body['tahun'] ,"status": "PROSES" ,"actived": True}, page_size=body['limit'], page_num=body['page'] + 1)
            else:
                count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"nomorberkas": body['nomor'] ,"tahunberkas": body['tahun'] ,"status": "PROSES" ,"actived": True})
                list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"receive": cookies['userid'] ,"nomorberkas": body['nomor'] ,"tahunberkas": body['tahun'] ,"status": "PROSES" ,"actived": True}, page_size=body['limit'], page_num=body['page'] + 1)

            self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
        else:
            self.redirect("/logout")


class InboxDetailController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, registerid=""):
        cookies = self.get_cookies_user()
        inbox = InboxModel(collection=self.CONNECTION.collection(database="registerdb", name="inbox"), service=options.service).get(filter={"_id": registerid})
        users = UserModel(collection=self.CONNECTION.collection(database="registerdb", name="users"), service=None).select(filter={"officeid": cookies['officeid'], "actived": True})
        self.render('node/detailmessange.html', info=inbox, users=users)


class InboxInfoDetailController(BaseController):


    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, registerid=""):
        cookies = self.get_cookies_user()
        
        info = {}
        pemohon = []
        pemilik = []

        inbox = InboxModel(collection=self.CONNECTION.collection(database="registerdb", name="inbox"), service=None)
        inboxResponse = inbox.get(filter={"_id": registerid})
        berkasid = inboxResponse['berkasid']
        yield gen.sleep(0.1)
        berkas = BerkasModel(collection=None, service=options.service)
        infoResponse = berkas.find(berkasid=berkasid)
        yield gen.sleep(0.1)
        simponiResponse = berkas.simponi(berkasid=berkasid)
        yield gen.sleep(0.1)
        produkResponse = berkas.produk(berkasid=berkasid)
        yield gen.sleep(0.1)
        daftarisianResponse = berkas.daftarisian(berkasid=berkasid)
        yield gen.sleep(0.1)
        if infoResponse.status_code == 200 and simponiResponse.status_code == 200 and produkResponse.status_code == 200 and daftarisianResponse.status_code == 200:
            info = infoResponse.json()['result']['infoberkas']
            simponi = simponiResponse.json()['result']
            produk = produkResponse.json()['result']
            daftarisian = daftarisianResponse.json()['result']
            for p in infoResponse.json()['result']['pemohon']:
                if p['typepemilikid'] == 'P':
                    pemohon.append(p)
                elif p['typepemilikid'] == 'M':
                    pemilik.append(p)
                    
            self.render("node/detailberkas.html", office=self.get_office_actived(cookies=cookies), inbox=inboxResponse, info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)
        else:
            self.render("page/error/400.html")