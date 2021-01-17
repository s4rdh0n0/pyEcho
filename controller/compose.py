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


class BerkasKKPController(BaseController):

    @tornado.web.authenticated
    def get(self):
        _connection = self.CONNECTION
        with _connection.client.start_session() as session:
            try:
                useractived = self.get_user_actived(cookies=self.get_cookies_user(), session=session)
                if useractived['actived']:
                    if UserModel(collection=_connection.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=useractived['_id'], role="REGIN", session=session) != None and useractived['actived']:
                        self.page_data['title'] = 'Berkas'
                        self.page_data['description'] = 'Daftar Berkas KKP'
                        self.render('page/kkp/daftarberkas.html', page=self.page_data, useractived=useractived)
                    else:
                        self.page_data['title'] = '403'
                        self.page_data['description'] = 'Access denied'
                        self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
                else:
                    self.redirect("/logout")
            except Exception as e:
                self.redirect("/logout")

class ComponseController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        _connection = self.CONNECTION
        with _connection.client.start_session() as session:
            try:
                useractived = self.get_user_actived(cookies=self.get_cookies_user(), session=session)
                if useractived['actived']:
                    if UserModel(collection=_connection.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=useractived['_id'], role="REGIN") != None and useractived['actived']:
                        self.page_data['title'] = 'Compose'
                        self.page_data['description'] = 'Register Berkas Masuk'
                        self.render('page/register/compose.html', page=self.page_data, useractived=useractived)
                    else:
                        self.page_data['title'] = '403'
                        self.page_data['description'] = 'Access denied'
                        self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
                else:
                    self.redirect("/logout")
            except Exception as e:
                self.redirect("/logout")

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        cookies = self.get_cookies_user()
        body = tornado.escape.json_decode(self.request.body)

        berkas = BerkasModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="berkas"), service=options.service)
        yield gen.sleep(0.1)
        response = berkas.search(officeid=cookies['officeid'], nomor=body['nomor'], tahun=body['tahun'])
        if response['data']['count']['Jumlah'] != 0:
            yield gen.sleep(0.1)
            count =berkas.count(filter={"_id": response['data']['result'][0]['berkasid']})
            if count == 0:
                self.write({'status': True, 'data': response['data']['result']})
            else:
                self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas {}/{} sudah terregister sebelumnya.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})
        else:
            self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas {}/{} tidak ada pada database https://kkp2.atrbpn.go.id/.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})


class ComponseDetailController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, berkasid=""):
        cookies = self.get_cookies_user()
        
        info = {}
        pemohon = []
        pemilik = []

        master = MasterModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="master"), service=None)
        region = RegionModel(collection=None, service=options.service)
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
            yield gen.sleep(0.1)
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
                    
            self.render("node/detailcompose.html", office=self.get_office_actived(cookies=cookies), desa=desa, status=status, info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)
        else:
            self.render("page/error/400.html")



    # REGISTER BERKAS MASUK
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # client request
        cookies = self.get_cookies_user()
        useractived = self.get_user_actived(cookies=cookies)
        body = tornado.escape.json_decode(self.request.body)

        offices = OfficeModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="offices"), service=None)
        region = RegionModel(collection=None, service=options.service)
        berkas =  BerkasModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="berkas"), service=options.service)
        register = RegisterModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="register"), service=None)
        master = MasterModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="master"), service=None)

        msg = ""
        status = False
        tipe = ""
        title = ""

        berkas_entity = berkas.find(berkasid=body['berkasid']).json()['result']
        yield gen.sleep(0.1)
        di_entity = berkas.daftarisian(berkasid=body['berkasid']).json()['result']
        yield gen.sleep(0.1)
        doc_entity = berkas.produk(berkasid=body['berkasid']).json()['result']
        yield gen.sleep(0.1)
        region_entity = region.all_desa(officeid=cookies['officeid']).json()['result']
        
        if berkas.count(filter={"_id": body['berkasid']}) == 0:
            desa_entity = {}
            for r in region_entity:
                if r['_id'] == body['desaid']:
                    desa_entity = r
                    break

            office_entity = offices.get(filter={"_id": cookies['officeid']})

            # Insert berkas
            schema_berkas = dict() 
            schema_berkas['_id'] = berkas_entity['infoberkas']['_id']
            schema_berkas['officeid'] = office_entity['_id']
            schema_berkas['officetype'] = office_entity['officetypeid']
            schema_berkas['officenama'] = office_entity['nama']
            schema_berkas['kecamatanid'] = desa_entity['wilayahinduk']['wilayahid']
            schema_berkas['kecamatancode'] = desa_entity['wilayahinduk']['kode']
            schema_berkas['namakecamatan'] = desa_entity['wilayahinduk']['nama']
            schema_berkas['desaid'] = desa_entity['_id']
            schema_berkas['desacode'] = desa_entity['kode']
            schema_berkas['namadesa'] = desa_entity['nama']
            schema_berkas['nomorberkas'] = berkas_entity['infoberkas']['nomor']
            schema_berkas['tahunberkas'] = berkas_entity['infoberkas']['tahun']
            schema_berkas['prosedur'] = berkas_entity['infoberkas']['prosedur']
            schema_berkas['kegiatan'] = berkas_entity['infoberkas']['kegiatan']
            schema_berkas['phone'] = body['phone']
            schema_berkas['email'] = body['email']
            schema_berkas['pemilik'] = berkas_entity['pemohon']
            schema_berkas['daftarisian'] = di_entity
            schema_berkas['document'] = doc_entity
            schema_berkas['status'] = body['status']
            berkas.add(schema=schema_berkas)

            schema_node = dict()
            schema_node['_id'] = uuid.uuid4().__str__()
            schema_node['register'] = offices.booking(officeid=cookies['officeid'], counter="REG")
            schema_node['job'] = 'REGIN'
            schema_node['officeid'] = schema_berkas['officeid']
            schema_node['berkasid'] = berkas_entity['infoberkas']['_id']
            schema_node['nomorberkas'] = schema_berkas['nomorberkas']
            schema_node['tahunberkas'] = schema_berkas['tahunberkas']
            schema_node['sender'] = cookies['userid']
            schema_node['sendername'] = useractived['nama']
            schema_node['senddate'] = datetime.datetime.now()
            schema_node['messsange'] = "Register berkas {}/{}. Tanggal. {}".format(berkas_entity['infoberkas']['nomor'], berkas_entity['infoberkas']['tahun'], schema_node['senddate'].strftime('%d-%m-%Y, %H:%M:%S'))
            schema_node['receivedate'] = None
            schema_node['receive'] = cookies['userid']
            schema_node['receivename'] = useractived['nama']
            schema_node['status'] = body['status']
            schema_node['actived'] = True
            register.add(schema=schema_node)

            msg = "Berkas {}/{} berhasil terregister.".format(schema_berkas['nomorberkas'], schema_berkas['tahunberkas'])
            status = True
            tipe = "info"
            title = '<strong>Info</strong> <br>'
        else:
            msg = "Berkas {}/{} sudah terregister sebelumnya.".format(berkas_entity['infoberkas']['nomor'], berkas_entity['infoberkas']['tahun'])
            status = False
            tipe = "minimalist"
            title = '<strong>Warning</strong> <br>'

        self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
