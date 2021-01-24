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

class InboxController(BaseController):
	
	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		try:
			if UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=self.useractived['_id'], role="REGISTER") != None:
				self.page_data['title'] = 'Inbox'
				self.page_data['description'] = 'Daftar Berkas Tunggakan'
				self.render('page/register/inbox.html', page=self.page_data, useractived=self.useractived)
			else:
				self.page_data['title'] = '403'
				self.page_data['description'] = 'Access denied'
				self.render("page/error/403.html", page=self.page_data,  useractived=self.useractived)
		except Exception as e:
			print(e)

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def post(self):
		list_response = []
		count_reponse = 0
		body = tornado.escape.json_decode(self.request.body)
		try:
			inbox = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)
			filter = {"officeid": self.get_cookies_user()['officeid'], "recieve": self.get_cookies_user()['userid'], "actived": True}
			if body['nomor'] != "":
				filter['nomorberkas'] = body['nomor']
			elif body['tahun'] != "":
				filter['tahunberkas'] = body['tahun']

			count_reponse = inbox.count(filter=filter)
			list_response = inbox.pagination(filter=filter, page_size = body['limit'], page_num = body['page'] + 1)
			
			self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
		except Exception as e:
			print(e)

	@tornado.web.authenticated
	def put(self):
		try:
			useractived = self.get_user_actived(cookies=self.get_cookies_user())
			body = tornado.escape.json_decode(self.request.body)

			berkas =  BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=options.service)
			pegawai = UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=None)
			register = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)

			msg = ""
			status = False
			tipe = ""
			title = ""

			berkas_entity = berkas.find(berkasid=body['berkasid']).json()['result']
			di_entity = berkas.daftarisian(berkasid=body['berkasid']).json()['result']
			doc_entity = berkas.produk(berkasid=body['berkasid']).json()['result']

			# Update Berkas.
			schema_berkas = berkas.get(filter={'_id': body['berkasid']})
			schema_berkas['pemilik'] = berkas_entity['pemohon']
			schema_berkas['daftarisian'] = di_entity
			schema_berkas['document'] = doc_entity
			berkas.update(filter={'_id': body['berkasid']}, schema=schema_berkas)

			node = register.get(filter={'_id': body['nodeid']})
			if node['actived']:
				node['actived'] = False
				register.update(filter={'_id': body['nodeid']}, schema=node)

				sender = pegawai.get(filter={'_id': useractived['_id']})
				recieve = pegawai.get(filter={'_id': body['petugasid']})
				schema_register = dict()
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


				msg = "{} <br> Berkas {}/{} berhasil tersimpan.".format(schema_berkas['officenama'], schema_berkas['nomorberkas'], schema_berkas['tahunberkas'])
				status = True
				tipe = "info"
				title = '<strong>Info</strong> <br>'

				self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
			else:
				msg = "{} <br> Berkas {}/{} berhasil tersimpan.".format(schema_berkas['officenama'], schema_berkas['nomorberkas'], schema_berkas['tahunberkas'])
				status = True
				tipe = "info"
				title = '<strong>Info</strong> <br>'
				self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
		except Exception as e:
			print(e)


class InboxDetailController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self, registerid=""):
		info = {}
		pemohon = None
		pemilik = []
		
		inbox = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)
		berkas = BerkasModel(collection=self.CONNECTION.collection(database='pyDatabase', name='berkas'), service=None)

		
		node = inbox.get(filter={"_id": registerid})
		yield gen.sleep(0.1)
		register = berkas.get(filter={'_id': node['berkasid']})
		yield gen.sleep(0.1)
		petugasResponse = UserModel(collection=self.CONNECTION.collection(database='pyDatabase', name='users'), service=None).select(filter={"actived": True, "_id": {"$ne":  self.get_cookies_user()['userid']}})
		yield gen.sleep(0.1)

		for p in register['pemilik']:
			if p['typepemilikid'] == 'P':
				pemohon = p
			elif p['typepemilikid'] == 'M':
				pemilik.append(p)
		
		if node['recievedate'] == None:
			node['recievedate'] = datetime.datetime.now()
			inbox.update(filter={"_id": node['_id']}, schema=node)
		
		self.render("node/detailinbox.html", office=self.get_office_actived(cookies=self.get_cookies_user()), register=register, node=node, petugas=petugasResponse, pemohon=pemohon)
