import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):
	
	def initialize(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())

	@tornado.web.authenticated
	def get(self):
		self.page_data['title'] = 'Dashboard'
		self.page_data['description'] = 'Rekapitulasi berkas register'
		self.render('page/home/dashboard.html', page=self.page_data, useractived=self.useractived)
