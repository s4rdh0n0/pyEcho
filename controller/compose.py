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
from model.register import RegisterModel
from model.node import NodeModel

class ComponseController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            if UserModel(collection=self.CONNECTION.collection(database="registerdb", name="users"), service=options.service).find_role(userid=useractived['_id'], role="REGIN") != None and useractived['actived']:
                self.page_data['title'] = 'Compose'
                self.page_data['description'] = 'Register New Berkas'
                self.render('page/register/compose.html', page=self.page_data, useractived=useractived)

            else:
                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
        else:
            self.redirect("/logout")


    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # client request
        cookies = self.get_cookies_user()
        body = tornado.escape.json_decode(self.request.body)

        berkas = BerkasModel(collection=None, service=options.service)
        response = berkas.search(officeid=cookies['officeid'], nomor=body['nomor'], tahun=body['tahun'])
        if response['status']:
            count = RegisterModel(collection=self.CONNECTION.collection(database="registerdb", name="register"), service=None).count(filter={"_id": response['data']['result'][0]['berkasid']})
            
            if count == 0:
                self.write({'status': True, 'data': response['data']['result']})
            else:
                self.write({'status': False, 'title': 'Warning', 'msg': 'Berkas sudah terregister sebelumnya.', 'type': 'minimalist'})
        else:
            self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas tidak ada pada database https://kkp2.atrbpn.go.id/.', 'type': 'minimalist'})



class ComponseDetailController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, berkasid=""):
        cookies = self.get_cookies_user()
        
        info = {}
        pemohon = []
        pemilik = []

        master = MasterModel(collection=self.CONNECTION.collection(database="registerdb", name="master"), service=None)
        region = RegionModel(collection=None, service=options.service)
        yield gen.sleep(0.1)
        berkas = BerkasModel(collection=None, service=options.service)
        yield gen.sleep(0.1)
        infoResponse = berkas.find(berkasid=berkasid)
        yield gen.sleep(0.1)
        simponiResponse = berkas.simponi(berkasid=berkasid)
        yield gen.sleep(0.1)
        produkResponse = berkas.produk(berkasid=berkasid)
        yield gen.sleep(0.1)
        daftarisianResponse = berkas.daftarisian(berkasid=berkasid)
        yield gen.sleep(0.1)
        regionResponse = region.all_desa(officeid=cookies['officeid'])
        yield gen.sleep(0.1)
        if infoResponse.status_code == 200 and simponiResponse.status_code == 200 and produkResponse.status_code == 200 and daftarisianResponse.status_code == 200:
            status = master.select(filter={"type": "OPERATION"})
            desa = regionResponse.json()['result']
            info = infoResponse.json()['result']['infoberkas']
            simponi = simponiResponse.json()['result']
            produk = produkResponse.json()['result']
            daftarisian = daftarisianResponse.json()['result']
            for p in infoResponse.json()['result']['pemohon']:
                if p['typepemilikid'] == 'P':
                    pemohon.append(p)
                elif p['typepemilikid'] == 'M':
                    pemilik.append(p)
                    
            self.render("node/detailberkas.html", office=self.get_office_actived(cookies=cookies), desa=desa, status=status, info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)
        else:
            self.render("page/error/400.html")
