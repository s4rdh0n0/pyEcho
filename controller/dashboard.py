import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.berkas import BerkasModel
from model.user import UserModel
from model.register import RegisterModel


class DashboardController(BaseController):

	def initialize(self):
		self.useractived = None

	@tornado.web.authenticated
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			berkas = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=None)
			register = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)
			petugas = UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=None)

			schema_berkas = {
				'masuk': berkas.count(filter={"officeid": self.get_cookies_user()['officeid']}),
				'proses': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'PROSES', 'actived': True}),
				'tunda': berkas.count(filter={'officeid': self.get_cookies_user()['officeid'], 'status': 'TUNDA', 'actived': True}),
				'selesai': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False})
			}
			cal_berkas = []
			for p in petugas.select(filter={'officeid': self.useractived['officeid']}):
				p['tunggakan'] = register.count({'recieve': p['_id'], 'actived': True})
				p['selesai'] = register.count({'recieve': p['_id'], 'actived': False})
				p['selesai_blm_terima'] = register.count({'recieve': p['_id'], 'actived': False, "recievedate": {"$ne": None}})
				cal_berkas.append(p)

			self.page_data['title'] = 'Dashboard'
			self.page_data['menu'] = 'dashboard'
			self.page_data['description'] = 'Rekapitulasi register berkas'
			self.render('page/home/dashboard.html', 
						page=self.page_data, 
						useractived=self.useractived,
						berkas=schema_berkas,
						cal_berkas=cal_berkas)

		except Exception as e:
			print(e)
