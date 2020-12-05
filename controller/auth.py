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
		djson = {"username": body["username"],
		         "password": body["password"]}
		try:
			responseJWT = requests.post('{}/{}/{}'.format(options.apis, 'auth', 'login'), json=djson)
			if responseJWT.status_code == 200:
				user = UserModel(officeid="none", host=options.apis, token=responseJWT.json()['token'])
				responseUser = user.find(typeid="username", userid=body["username"])

				self.result_validation['status'] = True
				self.result_validation['url'] = self.get_query_argument('next', u'/')
				self.result_validation['type'] = 'success'
				self.result_validation['msg'] = None
				self.save_cookies(body["username"], responseUser.json(), responseJWT.json()['token'])

			elif responseJWT.status_code == 401:
				self.result_validation['status'] = False
				self.result_validation['url'] = None
				self.result_validation['type'] = 'warning'
				self.result_validation['msg'] = 'Username or password not valid.'


		except Exception as e:
			self.write(e)
		finally:
			self.write(self.result_validation)

	def save_cookies(self, username="", userdatabase={}, token=""):
		self.cookies_data['userid'] = userdatabase['result']['_id']
		self.cookies_data['username'] = username
		self.cookies_data['pegawaiid'] = userdatabase['result']['pegawaiid']
		self.cookies_data['officeid'] = userdatabase['result']['officeid']
		self.cookies_data['token'] = token
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
