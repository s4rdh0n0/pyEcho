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
		self.useractived = None

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			if UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=self.useractived['_id'], role="REGIN") != None:
				self.page_data['title'] = 'Compose'
				self.page_data['menu'] = 'compose'
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
				self.write({'status': False, 'title': 'Warning', 'msg': 'Berkas {}/{} sudah terregister sebelumnya.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})
		else:
			self.write({'status': False, 'title': 'Warning', 'msg': 'Berkas {}/{} tidak ada pada database https://kkp2.atrbpn.go.id/.'.format(body['nomor'], body['tahun']), 'type': 'minimalist'})
	
	@tornado.web.authenticated
	@tornado.gen.coroutine
	def put(self):
		useractived = self.get_user_actived(cookies=self.get_cookies_user())
		body = tornado.escape.json_decode(self.request.body)

		offices = OfficeModel(collection=self.CONNECTION.collection(database="pyDatabase", name="offices"), service=None)
		berkas =  BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=options.service)
		region = RegionModel(collection=None, service=options.service)
		pegawai = UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=None)
		register = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)

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
		region_entity = region.all_desa(officeid=self.get_cookies_user()['officeid'])
		yield gen.sleep(0.1)
		if berkas.count(filter={"_id": body['berkasid']}) == 0:
			office_entity = offices.get(filter={"_id": self.get_cookies_user()['officeid']})

			region = dict()
			for d in region_entity.json()['result']:
				if body['desaid'] == d['_id']:
					region = d

			schema_berkas = dict()
			schema_berkas['_id'] = berkas_entity['infoberkas']['_id']
			schema_berkas['nomorregister'] = offices.booking(officeid=office_entity['_id'], counter='REG')
			schema_berkas['userregisterin'] = useractived['_id']
			schema_berkas['userregisterinname'] = useractived['nama']
			schema_berkas['userregisterindate'] = datetime.datetime.strptime(body['tglregister'], '%d/%m/%Y') 
			schema_berkas['officeid'] = office_entity['_id']
			schema_berkas['officetype'] = office_entity['officetypeid']
			schema_berkas['officenama'] = office_entity['nama']
			schema_berkas['kecamatanid'] = region['wilayahinduk']['wilayahid']
			schema_berkas['kecamatannama'] = region['wilayahinduk']['nama']
			schema_berkas['desaid'] = region['_id']
			schema_berkas['desanama'] = region['nama'] 
			schema_berkas['nomorberkas'] = berkas_entity['infoberkas']['nomor']
			schema_berkas['tahunberkas'] = berkas_entity['infoberkas']['tahun']
			schema_berkas['prosedur'] = berkas_entity['infoberkas']['prosedur']
			schema_berkas['kegiatan'] = berkas_entity['infoberkas']['kegiatan']
			schema_berkas['email'] = body['email']
			schema_berkas['phone'] = body['phone']
			schema_berkas['pemilik'] = berkas_entity['pemohon']
			schema_berkas['daftarisian'] = di_entity
			schema_berkas['document'] = doc_entity
			schema_berkas['status'] = 'PROSES'
			schema_berkas['actived'] = True
			berkas.add(schema=schema_berkas)
			yield gen.sleep(0.1)

			schema_register = dict()
			sender = pegawai.get(filter={'_id': useractived['_id']})
			recieve = pegawai.get(filter={'_id': body['petugasid']})
			schema_register['_id'] = uuid.uuid4().__str__()
			schema_register['officeid']   = schema_berkas['officeid']
			schema_register['officetype'] = schema_berkas['officetype']
			schema_register['officenama'] = schema_berkas['officenama']
			schema_register['berkasid'] = schema_berkas['_id']
			schema_register['nomorberkas'] = schema_berkas['nomorberkas']
			schema_register['tahunberkas'] = schema_berkas['tahunberkas']
			schema_register['prosedur'] = schema_berkas['prosedur']
			schema_register['kegiatan'] = schema_berkas['kegiatan']
			schema_register['sender'] = sender['_id']
			schema_register['sendername'] = sender['nama']
			schema_register['senderdate'] = datetime.datetime.now()
			schema_register['recieve'] = recieve['_id']
			schema_register['recievename'] = recieve['nama']
			schema_register['recievedate'] = None
			schema_register['messange'] = body['pesan']
			schema_register['actived'] = True
			register.add(schema=schema_register)

			msg = "{} <br> Berkas {}/{} <br> Register {} , Tgl.{}.".format(office_entity['nama'], schema_berkas['nomorberkas'], schema_berkas['tahunberkas'], schema_berkas['nomorregister'],body['tglregister'])
			status = True
			tipe = "info"
			title = '<strong>Info</strong> <br>'
		else:
			msg = "Berkas {}/{} sudah terregister sebelumnya.".format(berkas_entity['infoberkas']['nomor'], berkas_entity['infoberkas']['tahun'])
			status = False
			tipe = "minimalist"
			title = '<strong>Warning</strong> <br>'

		self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})


class DetailComposeController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self, berkasid=""):
		info = {}
		pemohon = []
		pemilik = []

		regionResponse = RegionModel(collection=None, service=options.service).all_desa(officeid=self.get_cookies_user()['officeid'])

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
		petugasResponse = UserModel(collection=self.CONNECTION.collection(database='pyDatabase', name='users'), service=None).select(filter={"actived": True, "_id": {"$ne":  self.get_cookies_user()['userid']}})

		info = infoResponse.json()['result']['infoberkas']
		simponi = simponiResponse.json()['result']
		produk = produkResponse.json()['result']
		daftarisian = daftarisianResponse.json()['result']
		for p in infoResponse.json()['result']['pemohon']:
			if p['typepemilikid'] == 'P':
				pemohon.append(p)
			elif p['typepemilikid'] == 'M':
				pemilik.append(p)

		self.render("node/detailcompose.html", office=self.get_office_actived(cookies=self.get_cookies_user()), region=regionResponse.json()['result'],  petugas=petugasResponse, info=info, pemohon=pemohon, pemilik=pemilik, simponi=simponi, produk=produk, daftarisian=daftarisian)


class ComposeListController(BaseController):

	def initialize(self):
		self.useractived = None

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			self.page_data['title'] = 'Table Compose'
			self.page_data['description'] = 'Daftar Register Berkas Masuk'
			self.render('page/register/compose_list.html', page=self.page_data, useractived=self.useractived)
		except Exception as e:
			print(e)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self):
		list_response = []
		count_reponse = 0
		body = tornado.escape.json_decode(self.request.body)
		try:
			inbox = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=None)
			filter = {"officeid": self.get_cookies_user()['officeid'], "actived": True}
			if body['nomor'] != "":
				filter['nomorberkas'] = body['nomor']
			elif body['tahun'] != "":
				filter['tahunberkas'] = body['tahun']

			count_reponse = inbox.count(filter=filter)
			list_response = inbox.pagination(filter=filter, page_size = body['limit'], page_num = body['page'] + 1)
			
			self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
		except Exception as e:
			print(e)


class DetailComposeListController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self, berkasid=""):
		pemohon = None
		pemilik = []
		
		berkas = BerkasModel(collection=self.CONNECTION.collection(database='pyDatabase', name='berkas'), service=None)
		riwayat = RegisterModel(collection = self.CONNECTION.collection(database='pyDatabase', name='register'), service=None).select(filter={"berkasid": berkasid})

		register = berkas.get(filter={'_id': berkasid})
		for p in register['pemilik']:
			if p['typepemilikid'] == 'P':
				pemohon = p
			elif p['typepemilikid'] == 'M':
				pemilik.append(p)
		
		self.render("node/detilberkasmasuk.html", office=self.get_office_actived(cookies=self.get_cookies_user()), register=register, riwayat=riwayat, pemohon=pemohon)

