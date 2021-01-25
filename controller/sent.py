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
	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		try:
			if UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=options.service).find_role(userid=self.useractived['_id'], role="REGISTER") != None:
				self.page_data['title'] = 'Sent'
				self.page_data['description'] = 'Daftar Berkas Terkirim'
				self.render('page/register/sent.html', page=self.page_data, useractived=self.useractived)
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
			filter = {"officeid": self.get_cookies_user()['officeid'], "sender": self.get_cookies_user()['userid']}
			if body['nomor'] != "":
				filter['nomorberkas'] = body['nomor']
			elif body['tahun'] != "":
				filter['tahunberkas'] = body['tahun']

			count_reponse = inbox.count(filter=filter)
			list_response = inbox.pagination(filter=filter, page_size = body['limit'], page_num = body['page'] + 1)
			
			self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
		except Exception as e:
			print(e)



class SentDetailController(BaseController):

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

		for p in register['pemilik']:
			if p['typepemilikid'] == 'P':
				pemohon = p
			elif p['typepemilikid'] == 'M':
				pemilik.append(p)
		
		self.render("node/detailsent.html", office=self.get_office_actived(cookies=self.get_cookies_user()), register=register, node=node, pemohon=pemohon)
