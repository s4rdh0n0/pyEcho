import json
import requests

# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options


# Controller
import controller
from controller.init import BaseController


class SignInController(BaseController):

	result = {
		'status': False,
		'url': options.api + "/login",
		'type': None,
		'msg': 'Username or password not valid.',
	}

	def get(self):
		try:
			self.render('auth/login.html')
		except Exception as e:
			print("Error: {}".format(e))

	def post(self):
		body = tornado.escape.json_decode(self.request.body)
		djson = {"username": body["username"],
		         "password": body["password"]}
		try:
			validation = requests.post('{}/{}/{}'.format(options.api, 'auth', 'login'), json=djson)
			if validation.status_code == 200:
				self.result['status'] = True
				self.result['url'] = None
				self.result['type'] = 'success'
				self.result['msg'] = None

				print(validation.json())
			elif validation.status_code == 401:
				self.result['status'] = False
				self.result['url'] = options.api + "/login"
				self.result['type'] = 'warning'
				self.result['msg'] = 'Username or password not valid.'
		except Exception as e:
			self.write(e)
		finally:
			self.write(self.result)

	def save_cookies(self, validation = {}):
		pass
