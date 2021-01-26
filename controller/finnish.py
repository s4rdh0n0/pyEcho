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
from model.user import UserModel
from model.berkas import BerkasModel

class FinnishListController(BaseController):

	def initialize(self):
		self.useractived = None


	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			self.page_data['title'] = 'Table Finnish'
			self.page_data['description'] = 'Daftar Berkas Keluar'
			self.render('page/register/finnish.html', page=self.page_data, useractived=self.useractived)
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
			filter = {"officeid": self.get_cookies_user()['officeid'], "actived": False}
			if body['nomor'] != "":
				filter['nomorberkas'] = body['nomor']
			elif body['tahun'] != "":
				filter['tahunberkas'] = body['tahun']

			count_reponse = inbox.count(filter=filter)
			list_response = inbox.pagination(filter=filter, page_size = body['limit'], page_num = body['page'] + 1)
			
			self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
		except Exception as e:
			print(e)
