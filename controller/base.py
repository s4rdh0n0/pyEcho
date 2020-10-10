import requests

# Tornado Framework
import tornado
import tornado.escape
import tornado.web
from tornado.options import options, define

# Model
from model.user import UserModel


# Global variable
define("apis", default="http://localhost:8000", help="web service")
define("cookies", default="pyEchoCookies", help="web")


class BaseController(tornado.web.RequestHandler):
   
	"""  """
	
	static_file = options.apis + '/static/'

	cookies_data = {
		'userid': None,
		'username': None,
		'pegawaiid': None,
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
		user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
		return user.pegawai(username=cookies['username'])

	def get_user_role(self, cookies={}, key=""):
		user = UserModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
		return user.find_role(typeid="_id", userid=cookies['userid'], key=key)

	def get_office_actived(self, cookies={}):
		dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
		param = 'officeid={}&typeid=_id'.format(cookies['officeid'])
		return requests.get('{}/offices/find?{}'.format(options.apis, param), headers=dheader)
	
	def refresh_cookies(self, cookies={}):
		dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
		response = requests.get('{}/{}/{}'.format(options.apis, 'auth', 'refresh_token'), headers=dheader)
		if response.status_code == 200:
			cookies['token'] = response.json()['token']
			self.set_secure_cookie(options.cookies, tornado.escape.json_encode(cookies))
		else:
			self.redirect("/login")
