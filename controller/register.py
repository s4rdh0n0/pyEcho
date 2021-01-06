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
        if response['data']['count']['Jumlah'] != 0:
            count = RegisterModel(collection=self.CONNECTION.collection(database="registerdb", name="register"), service=None).count(filter={"_id": response['data']['result'][0]['berkasid']})
            if count == 0:
                self.write({'status': True, 'data': response['data']['result']})
            else:
                self.write({'status': False, 'title': 'Warning', 'msg': 'Berkas sudah terregister sebelumnya.', 'type': 'minimalist'})
        else:
            self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas tidak ada pada database https://kkp2.atrbpn.go.id/.', 'type': 'minimalist'})


class InboxController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            if len(useractived['role']) != 0 and useractived['actived']:
                self.page_data['title'] = 'Inbox'
                self.page_data['description'] = 'Inbox Register Berkas'
                self.render('page/register/inbox.html', page=self.page_data, useractived=useractived)

            else:
                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
        else:
            self.redirect("/logout")

    
    def post(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            # client request
            cookies = self.get_cookies_user()
            body = tornado.escape.json_decode(self.request.body)

            list_response = []
            count_reponse = 0

            node  = self.CONNECTION.collection(database="registerdb", name="node")
            register = RegisterModel(collection=self.CONNECTION.collection(database="registerdb", name="register"), node=node, service=None)


            count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"pegawaiactived": cookies['userid']})
            list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"pegawaiactived": cookies['userid']},page_size=count_reponse, page_num=body['page'] + 1)

            self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
        else:
            self.redirect("/logout")

class RegisterBerkasViewController(BaseController):

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

    # REGISTER BERKAS MASUK
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
        # client request
        cookies = self.get_cookies_user()
        body = tornado.escape.json_decode(self.request.body)

        offices = OfficeModel(collection=self.CONNECTION.collection(database="registerdb", name="offices"), service=None)
        yield gen.sleep(0.1)
        region = RegionModel(collection=None, service=options.service).all_desa(officeid=cookies['officeid']).json()['result']
        yield gen.sleep(0.1)
        berkas =  BerkasModel(collection=None, service=options.service)
        yield gen.sleep(0.1)
        register = RegisterModel(collection=self.CONNECTION.collection(database="registerdb", name="register"), service=None)
        yield gen.sleep(0.1)
        node = NodeModel(collection=self.CONNECTION.collection(database="registerdb", name="node"), service=None)
        yield gen.sleep(0.1)

        msg = ""
        status = False
        tipe = ""
        title = ""
        berkas_entity = berkas.find(berkasid=body['berkasid']).json()['result']
        di_entity = berkas.daftarisian(berkasid=body['berkasid']).json()['result']
        doc_entity = berkas.produk(berkasid=body['berkasid']).json()['result']
        
        if register.count(filter={"_id": body['berkasid']}) == 0:
            desa_entity = {}
            for r in region:
                if r['_id'] == body['desaid']:
                    desa_entity = r
                    break

            office_entity = offices.get(filter={"_id": cookies['officeid']})

            schema_node = node.schema
            schema_node['_id'] =  uuid.uuid4().__str__()
            yield gen.sleep(0.1)
            schema_node['register'] = offices.booking(officeid=cookies['officeid'],counter="REG")
            schema_node['berkasid'] = berkas_entity['infoberkas']['_id']
            schema_node['type'] = "REGIN"
            schema_node['operator'] = cookies['userid']
            schema_node['startdate'] = datetime.datetime.now()
            schema_node['status'] = False
            node.add(schema=schema_node)
            yield gen.sleep(0.1)

            schema = register.schema
            schema['_id'] = berkas_entity['infoberkas']['_id']
            schema['pegawaiactived'] = cookies['userid']
            schema['nodeactived'] = schema_node['_id']
            schema['officeid'] = office_entity['_id']
            schema['officetype'] = office_entity['officetypeid']
            schema['officenama'] = office_entity['nama']
            schema['kecamatanid'] = desa_entity['wilayahinduk']['wilayahid']
            schema['kecamatancode'] = desa_entity['wilayahinduk']['kode']
            schema['namakecamatan'] = desa_entity['wilayahinduk']['nama']
            schema['desaid'] = desa_entity['_id']
            schema['desacode'] = desa_entity['kode']
            schema['namadesa'] = desa_entity['nama']
            schema['nomorberkas'] = berkas_entity['infoberkas']['nomor']
            schema['tahunberkas'] = berkas_entity['infoberkas']['tahun']
            schema['prosedur'] = berkas_entity['infoberkas']['prosedur']
            schema['kegiatan'] = berkas_entity['infoberkas']['kegiatan']
            schema['phone'] = body['phone']
            schema['email'] = body['email']
            schema['startdate'] = datetime.datetime.strptime(berkas_entity['infoberkas']['startdate'] , '%Y-%m-%dT%H:%M:%S%z')
            schema['pemilik'] = berkas_entity['pemohon']
            schema['daftarisian'] = di_entity
            schema['document'] = doc_entity
            schema['status'] = body['status']
            schema['keterangan'] = body['keterangan']
            schema['actived'] = True
            register.add(schema=schema)

            msg = "Berkas {}/{} berhasil disimpan.".format(schema['nomorberkas'], schema['tahunberkas'])
            status = True
            tipe = "info"
            title = '<strong>Info</strong> <br>'
        else:
            msg = "Berkas {}/{} sudah terregister sebelumnya.".format(berkas_entity['infoberkas']['nomor'], berkas_entity['infoberkas']['tahun'])
            status = False
            tipe = "minimalist"
            title = '<strong>Warning</strong> <br>'

        self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
