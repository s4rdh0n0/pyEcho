import requests

import tornado.escape
import tornado.web
from tornado.options import options, define

define("apis", default="http://localhost:8000", help="web service")
define("cookies", default="pyEchoCookies", help="web")


class BaseController(tornado.web.RequestHandler):
   
	"""  """
	
	cookies_data = {
		'username': None,
		'token': None,
	}

	def get_cookies_user(self):
		return tornado.escape.json_decode(self.get_secure_cookie(options.cookies))

	def get_current_user(self):
		return self.get_secure_cookie(options.cookies)

	def get_user_actived(self):
		cookies = self.get_cookies_user()
		dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
		respon = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?username=', cookies['username']), headers=dheader)

		return respon

	def refresh_cookies(self, token=""):
		dheader = {'Authorization': 'Bearer {}'.format(token)}
		respon = requests.get('{}/{}/{}'.format(options.apis, 'auth', 'refresh_token'), headers=dheader)
		if respon.status_code == 200:
			cookies = self.get_cookies_user()
			cookies['token'] = respon.json()['token']
			self.set_secure_cookie(options.cookies, tornado.escape.json_encode(cookies))
