import json
import requests

# Tornado Framework
import tornado.gen
import tornado.web
import tornado.escape
from tornado.options import options


# Controller
from controller.base import BaseController


class SignInController(BaseController):

	result_validation = {
		'status': False,
		'url': options.apis + "/login",
		'type': None,
		'msg': 'Username or password not valid.',
	}

	def get(self):
		try:
			self.render('auth/login.html')
		except Exception as e:
			self.write(e)


	def post(self):
		body = tornado.escape.json_decode(self.request.body)
		djson = {"username": body["username"],
		         "password": body["password"]}
		try:
			respon = requests.post('{}/{}/{}'.format(options.apis, 'auth', 'login'), json=djson)
			if respon.status_code == 200:
				self.result_validation['status'] = True
				self.result_validation['url'] = self.get_query_argument('next', '/')
				self.result_validation['type'] = 'success'
				self.result_validation['msg'] = None

				self.save_cookies(body["username"],respon.json())
			elif respon.status_code == 401:
				self.result_validation['status'] = False
				self.result_validation['url'] = None
				self.result_validation['type'] = 'warning'
				self.result_validation['msg'] = 'Username or password not valid.'
		except Exception as e:
			self.write(e)
		finally:
			self.write(self.result_validation)

	def save_cookies(self, username = "",validation = {}):
		dheader = {'Authorization': 'Bearer {}'.format(validation['token'])}
		respon = requests.get('{}/{}{}&type=username'.format(options.apis, 'offices/users/find?id=', username), headers=dheader)
		if respon.status_code == 200:
			self.cookies_data['userid'] = respon.json()['result']['_id']
			self.cookies_data['username'] = respon.json()['result']['username']
			self.cookies_data['token'] = validation['token']
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
