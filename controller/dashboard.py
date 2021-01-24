import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.berkas import BerkasModel


class DashboardController(BaseController):
	
	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	def get(self):
		try:
			berkas = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=None)

			self.page_data['title'] = 'Dashboard'
			self.page_data['description'] = 'Rekapitulasi register berkas'
			self.render('page/home/dashboard.html', 
						page=self.page_data, 
						useractived=self.useractived,
						berkasmasuk=berkas.count(filter={"officeid": self.get_cookies_user()['officeid']}),
						berkasproses=berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'PROSES', 'actived': True}),
						berkastunda=berkas.count(filter={'officeid': self.get_cookies_user()['officeid'], 'status': 'TUNDA', 'actived': True}),
						berkasselesai=berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False}))
		except Exception as e:
			print(e)
