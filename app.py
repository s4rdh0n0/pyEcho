# Python Default
import os

# Tornado Framework
import tornado.web
import tornado.options
import tornado.gen
import tornado.locks
from tornado.options import define, options

import controller.auth

class Application(tornado.web.Application):

   handlers = [(r"/login", controller.auth.SignInController)]

   def __init__(self):

      settings = dict(
          title='pyEcho',
          version='1.0.0',
          template_path=os.path.join(options.dir, 'view'),
          static_path=os.path.join(options.dir, 'assets'),
          xsrf_cookies=True,
          cookie_secret='16b56537-b94e-49bc-9f98-9be58f0b2d28',
          login_url=r"/login",
          debug=True,
      )

      super(Application, self).__init__(self.handlers, **settings)
