import json
import requests

# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options


# Controller
import controller
from controller.base import BaseController


class SignInController(BaseController):

	result_validation = {
		'status': False,
		'url': options.apis + "/login",
		'type': None,
		'msg': 'Username or password not valid.',
	}

	cookies = {
		'username': None,
		'token': None,
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
				self.result_validation['url'] = None
				self.result_validation['type'] = 'success'
				self.result_validation['msg'] = None

				self.save_cookies(body["username"],respon.json())
			elif respon.status_code == 401:
				self.result_validation['status'] = False
				self.result_validation['url'] = options.apis + "/login"
				self.result_validation['type'] = 'warning'
				self.result_validation['msg'] = 'Username or password not valid.'
		except Exception as e:
			self.write(e)
		finally:
			self.write(self.result_validation)


	def save_cookies(self, username = "",validation = {}):
		dheader = {'Authorization': 'Bearer {}'.format(validation['token'])}
		respon = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?username=', username), headers=dheader)
		if respon.status_code == 200:
			self.cookies['username'] = respon.json()['result']['username']
			self.cookies['token'] = validation['token']
			self.set_secure_cookie(options.cookies, tornado.escape.json_encode(self.cookies))
