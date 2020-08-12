import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):

    @tornado.web.authenticated
    def get(self):
        try:
            respon = self.get_user_actived()
            if respon == 200:
                self.render('dashboard.html', user=respon.json()['result'])
        except Exception as e:
        	self.write(e)
