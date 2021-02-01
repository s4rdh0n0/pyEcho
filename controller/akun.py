# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options
from tornado import gen

# Controller
from controller.base import BaseController

# Model
from model.office import OfficeModel
from model.user import UserModel



class AkunSayaController (BaseController):

	def initialize(self):
		self.useractived = None

	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			self.page_data['title'] = 'Profile'
			self.page_data['menu'] = 'profile'
			self.page_data['description'] = 'Biodata'
			self.render('page/akun/profile.html', page=self.page_data, useractived=self.useractived)
		except Exception as e:
			print(e)

class GantiPasswordController(BaseController):

	def initialize(self):
		self.useractived = None

	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			self.page_data['title'] = 'Ganti Password'
			self.page_data['menu'] = 'ganti password'
			self.page_data['description'] = ''
			self.render('page/akun/ganti_password.html', page=self.page_data, useractived=self.useractived)
		except Exception as e:
			print(e)
