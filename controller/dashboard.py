from datetime import date, datetime

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

			today = date.today()
			start = datetime(
				year=today.year,
				month=today.month,
				day=today.day,
			)
			end = datetime.now()
			schema_berkas = {
				'masuk': berkas.count(filter={"officeid": self.get_cookies_user()['officeid']}),
				'masuk_harini': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'userregisterindate': {'$gte': start, '$lt': end}}),
				'proses': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'PROSES', 'actived': True}),
				'tunda': berkas.count(filter={'officeid': self.get_cookies_user()['officeid'], 'status': 'TUNDA', 'actived': True}),
				'selesai': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False}),
                'selesai_hariini': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False, 'finnishdate': {'$gte': start, '$lt': end}})
			}
			cal_berkas = []
			index = 1
			for p in petugas.select(filter={'officeid': self.useractived['officeid']}):
				p['index'] = index
				p['tunggakan'] = register.count({'recieve': p['_id'], 'actived': True})
				p['tunggakan_sdh_diterima'] = register.count({'recieve': p['_id'], 'recievedate':{'$ne': None }, 'actived': True})
				p['selesai'] = register.count({'recieve': p['_id'], 'actived': False})
				index = index + 1
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
