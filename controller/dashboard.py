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
            if self.refresh_cookies():
                respon = self.get_user_actived()
                if respon.status_code == 200:
                    self.render('dashboard.html', useractived=respon.json()['result'])
        except Exception as e:
        	self.write(e)
