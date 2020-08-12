import tornado.escape


from tornado.web import RequestHandler
from tornado.options import options, define

define("apis", default="http://localhost:8000", help="web service")
define("cookies", default="pyEchoCookies", help="web")

class BaseController(RequestHandler):
   
	"""  """

	def get_cookies_user(self):
		return tornado.escape.json_decode(self.get_secure_cookie(options.cookies))

	def get_current_user(self):
		return self.get_secure_cookie(options.cookies)
