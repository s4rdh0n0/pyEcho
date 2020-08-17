import requests

import tornado.escape
import tornado.web
from tornado.options import options, define


define("apis", default="http://localhost:8000", help="web service")
define("cookies", default="pyEchoCookies", help="web")


class BaseController(tornado.web.RequestHandler):
   
	"""  """
	
	cookies_data = {
		'userid': None,
		'username': None,
		'officeid': None,
		'token': None,
	}

	page_data = {
		'title': None,
		'description': None,
	}


	"""  """

	def get_cookies_user(self):
		return tornado.escape.json_decode(self.get_secure_cookie(options.cookies))

	def get_current_user(self):
		return self.get_secure_cookie(options.cookies)

	def get_user_actived(self, cookies={}):
		dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
		
		return requests.get('{}/{}'.format(options.apis, 'offices/users/actived'), headers=dheader)

	def get_office_actived(self, cookies={}):
		dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
		param = 'id={}&type=officeid'.format(cookies['officeid'])

		return requests.get('{}/offices/find?{}'.format(options.api, param), headers=dheader)
	
	def refresh_cookies(self, cookies={}):
		try:
			dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
			respon = requests.get('{}/{}/{}'.format(options.apis, 'auth', 'refresh_token'), headers=dheader)
			
			if respon.status_code != 200:
				self.redirect("/login")
		except:
			self.redirect("/login")
