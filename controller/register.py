import requests

# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.region import RegionModel
from model.user import UserModel
from model.berkas import BerkasModel
from model.region import RegionModel


class ComponseController(BaseController):

    @tornado.web.authenticated
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            collection = self.CONNECTION.collection(database="registerdb", name="users")
            if UserModel(collection=collection, service=options.service).find_role(userid=useractived['_id'], role="REGIN") != None and useractived['actived']:

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
    def post(self):
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        berkas = BerkasModel(collection=None, service=options.service)
        response = berkas.search(officeid=cookies['officeid'], nomor=body['nomor'], tahun=body['tahun'])
        if response['status']:
            if response['data']['result'] == None:
                self.write({'status': False, 'data': None})
            else:
                self.write({'status': True, 'data': response['data']['result']})
        else:
            self.write({'status': False, 'data': None})


class RegisterBerkasViewController(BaseController):
    
    @tornado.web.authenticated
    def get(self, berkasid=""):
        cookies = self.get_cookies_user()
        
        info = {}
        pemohon = []
        pemilik = []

        region = RegionModel(collection=None, service=options.service)
        berkas = BerkasModel(collection=None, service=options.service)
        infoResponse = berkas.find(berkasid=berkasid)
        simponiResponse = berkas.simponi(berkasid=berkasid)
        produkResponse = berkas.produk(berkasid=berkasid)
        daftarisianResponse = berkas.daftarisian(berkasid=berkasid)
        regionResponse = region.all_desa(officeid=cookies['officeid'])

        if infoResponse.status_code == 200 and simponiResponse.status_code == 200 and produkResponse.status_code == 200 and daftarisianResponse.status_code == 200:
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
                    
            self.render("node/detailberkas.html", office=self.get_office_actived(cookies=cookies), desa=desa, info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)
        else:
            self.render("page/error/400.html")