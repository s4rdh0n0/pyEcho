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


class ComponseController(BaseController):

	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		try:
			if UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=self.useractived['_id'], role="REGIN") != None:
				self.page_data['title'] = 'Compose'
				self.page_data['description'] = 'Register Berkas Masuk'
				self.render('page/register/compose.html', page=self.page_data, useractived=self.useractived)
			else:
				self.page_data['title'] = '403'
				self.page_data['description'] = 'Access denied'
				self.render("page/error/403.html", page=self.page_data,  useractived=self.useractived)
		except Exception as e:
			print(e)


	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self):
		body = tornado.escape.json_decode(self.request.body)
		berkas_kkp = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=options.service)
		response = berkas_kkp.search(officeid=self.get_cookies_user()['officeid'], nomor=body['nomor'], tahun=body['tahun'])
		if response['data']['count']['Jumlah'] != 0:
			count = berkas_kkp.count(filter={"_id": response['data']['result'][0]['berkasid']})
			if count == 0:
				self.write({'status': True, 'data': response['data']['result']})
			else:
				self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas {}/{} sudah terregister sebelumnya.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})
		else:
			self.write({'status': False, 'title': 'Warning', 'msg': 'Nomor berkas {}/{} tidak ada pada database https://kkp2.atrbpn.go.id/.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})


class BerkasMasukController(BaseController):

	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		try:
			if UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=self.useractived['_id'], role="REGIN") != None:
				self.page_data['title'] = 'Compose List'
				self.page_data['description'] = 'Daftar Berkas Masuk'
				self.render('page/register/compose_list.html', page=self.page_data, useractived=self.useractived)
			else:
				self.page_data['title'] = '403'
				self.page_data['description'] = 'Access denied'
				self.render("page/error/403.html", page=self.page_data,  useractived=self.useractived)
		except Exception as e:
			print(e)

	
	@tornado.web.authenticated
	def post(self):
		list_response = []
		count_reponse = 0
		body = tornado.escape.json_decode(self.request.body)
		try:
			inbox = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=None)
			if body['nomor'] == "" and body['tahun'] == "":
				count_reponse = inbox.count(filter={"officeid": self.get_cookies_user()['officeid'] , "status": "REGIN" ,"actived": True})
				list_response = inbox.pagination(filter={"officeid": self.get_cookies_user()['officeid'], "status": "REGIN", "actived": True}, page_size = body['limit'], page_num = body['page'] + 1)
			elif body['nomor']  != "" and body['tahun'] == "":
				count_reponse = inbox.count(filter={"officeid": self.get_cookies_user()['officeid'], "nomorberkas": body['nomor'], "status": "REGIN", "actived": True})
				list_response = inbox.pagination(filter={"officeid": self.get_cookies_user()['officeid'], "nomorberkas": body['nomor'], "status": "REGIN", "actived": True}, page_size = body['limit'], page_num = body['page'] + 1)
			elif body['nomor'] == "" and body['tahun'] != "":
				count_reponse = inbox.count(filter={"officeid": self.get_cookies_user()['officeid'], "tahunberkas": body['tahun'], "status": "REGIN", "actived": True})
				list_response = inbox.pagination(filter={"officeid": self.get_cookies_user()['officeid'], "tahunberkas": body['tahun'], "status": "REGIN", "actived": True}, page_size = body['limit'], page_num = body['page'] + 1)
			elif body['nomor'] != "" and body['tahun'] != "":
				count_reponse = inbox.count(filter={"officeid": self.get_cookies_user()['officeid'], "nomorberkas":body['nomor'] ,"tahunberkas": body['tahun'], "status": "REGIN", "actived": True})
				list_response = inbox.pagination(filter={"officeid": self.get_cookies_user()['officeid'], "nomorberkas":body['nomor'] ,"tahunberkas": body['tahun'], "status": "REGIN", "actived": True}, page_size = body['limit'], page_num = body['page'] + 1)
			self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
		except Exception as e:
			print(e)



class DetailBerkasController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self, berkasid=""):		
		info = {}
		pemohon = []
		pemilik = []

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
					
			self.render("node/detailberkas.html", office=self.get_office_actived(cookies=self.get_cookies_user()), info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)
		else:
			self.render("page/error/400.html")


	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self):
		useractived = self.get_user_actived(cookies=self.get_cookies_user())
		body = tornado.escape.json_decode(self.request.body)

		offices = OfficeModel(collection=self.CONNECTION.collection(database="pyDatabase", name="offices"), service=None)
		berkas =  BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=options.service)

		msg = ""
		status = False
		tipe = ""
		title = ""

		berkas_entity = berkas.find(berkasid=body['berkasid']).json()['result']
		yield gen.sleep(0.1)
		di_entity = berkas.daftarisian(berkasid=body['berkasid']).json()['result']
		yield gen.sleep(0.1)
		doc_entity = berkas.produk(berkasid=body['berkasid']).json()['result']
		
		if berkas.count(filter={"_id": body['berkasid']}) == 0:
			office_entity = offices.get(filter={"_id": self.get_cookies_user()['officeid']})

			# Insert berkas
			schema_berkas = dict() 
			schema_berkas['_id'] = berkas_entity['infoberkas']['_id']
			schema_berkas['nomorregister'] = offices.booking(officeid=office_entity['_id'], counter='REG')
			schema_berkas['userregisterin'] = useractived['_id']
			schema_berkas['userregisterinname'] = useractived['nama']
			schema_berkas['userregisterindate'] = datetime.datetime.now()
			schema_berkas['officeid'] = office_entity['_id']
			schema_berkas['officetype'] = office_entity['officetypeid']
			schema_berkas['officenama'] = office_entity['nama']
			schema_berkas['nomorberkas'] = berkas_entity['infoberkas']['nomor']
			schema_berkas['tahunberkas'] = berkas_entity['infoberkas']['tahun']
			schema_berkas['prosedur'] = berkas_entity['infoberkas']['prosedur']
			schema_berkas['kegiatan'] = berkas_entity['infoberkas']['kegiatan']
			schema_berkas['pemilik'] = berkas_entity['pemohon']
			schema_berkas['daftarisian'] = di_entity
			schema_berkas['document'] = doc_entity
			schema_berkas['status'] = 'REGIN'
			schema_berkas['actived'] = True
			berkas.add(schema=schema_berkas)

			msg = "Berkas {}/{} berhasil tersimpan.".format(schema_berkas['nomorberkas'], schema_berkas['tahunberkas'])
			status = True
			tipe = "info"
			title = '<strong>Info</strong> <br>'
		else:
			msg = "Berkas {}/{} sudah tersimpan sebelumnya.".format(berkas_entity['infoberkas']['nomor'], berkas_entity['infoberkas']['tahun'])
			status = False
			tipe = "minimalist"
			title = '<strong>Warning</strong> <br>'

		self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
