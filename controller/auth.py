import json
import requests

# Tornado Framework
import tornado.gen
import tornado.web
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.user import UserModel

class SignInController(BaseController):

	result_validation = {
		'status': False,
		'url': "/login",
		'type': None,
		'msg': 'Username or password not valid.',
	}

	def get(self):
		self.render('page/auth/login.html', static_file=self.static_file)

	def post(self):
		body = tornado.escape.json_decode(self.request.body)
		try:
			collection = self.CONNECTION.collection(database="registerdb", name="users")
			user = UserModel(collection=collection, service=options.service)
			responseAUTH = user.auth(username= body['username'], password= body['password'])
			if responseAUTH:
				result = user.get(filter={"username": body['username'], "password": body['password']})

				self.result_validation['status'] = True
				self.result_validation['url'] = self.get_query_argument('next', u'/')
				self.result_validation['type'] = 'success'
				self.result_validation['msg'] = None
				self.save_cookies(result)

			else:
				self.result_validation['status'] = False
				self.result_validation['url'] = None
				self.result_validation['type'] = 'warning'
				self.result_validation['msg'] = 'Gagal login. Nama pengguna atau kata sandi yang anda masukkan salah.'


		except Exception as e:
			self.write(e)
		finally:
			self.write(self.result_validation)

	def save_cookies(self, userdatabase={}):
		self.cookies_data['userid'] = userdatabase['_id']
		self.cookies_data['username'] = userdatabase['username']
		self.cookies_data['pegawaiid'] = userdatabase['pegawaiid']
		self.cookies_data['officeid'] = userdatabase['officeid']
		self.set_secure_cookie(options.cookies, tornado.escape.json_encode(self.cookies_data))

class SignOutController(BaseController):

	@tornado.web.authenticated
	def get(self):
		self.clear_cookie(options.cookies)
		self.redirect("/login")

class NotFoundController (BaseController):

	@tornado.web.authenticated
	def get(self):
		try:
		    respon = self.get_user_actived()
		    if  respon.status_code == 200:
		        self.page_data['title'] = 'Error 404'
		        self.page_data['description'] = 'Page not found'
		        self.render('error/404.html', page=self.page_data, useractived=respon.json()['result'])
		except Exception as e:
			self.write(e)
