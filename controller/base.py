import requests

# Tornado Framework
import tornado
import tornado.escape
import tornado.web
from tornado.options import options, define

# Model
from model.base import ConnectionModel
from model.user import UserModel
from model.office import OfficeModel


# Global variable
define("db_host", default="localhost", help="Mongo DB")
define("db_port", default="27017", help="Mongo DB")
define("db_user", default="1228_adminregister", help="Mongo DB")
define("db_password", default="1228trenggalek", help="Mongo DB")

define("service", default="http://localhost:8000", help="web service")
define("cookies", default="pyEchoCookies", help="web")





class BaseController(tornado.web.RequestHandler):
	
	static_file = options.service + '/static/'

	CONNECTION = ConnectionModel(username=options.db_user, password=options.db_password, server=options.db_host, port=options.db_port)

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


	def get_cookies_user(self):
		return tornado.escape.json_decode(self.get_secure_cookie(options.cookies))

	def get_current_user(self):
		return self.get_secure_cookie(options.cookies)

	def get_user_actived(self, cookies={}):
		collection = self.CONNECTION.collection(database="registerdb", name="users")
		user = UserModel(collection=collection, service=options.service)
		return user.get(filter={"username": cookies['username']})

	def get_user_role(self, cookies:{}, key:str):
		collection = self.CONNECTION.collection(database="registerdb", name="users")
		user = UserModel(collection=collection, service=options.service)
		return user.find_role(usersid=cookies['userid'], role=key)

	def get_office_actived(self, cookies={}):
		collection = self.CONNECTION.collection(database="registerdb", name="offices")
		office = OfficeModel(collection=collection, service=options.service)
		
		return office.get(filter={"officeid": cookies['officeid']})