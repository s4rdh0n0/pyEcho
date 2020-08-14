import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):

    @tornado.web.authenticated
    def get(self):
        self.refresh_cookies()
        try:
            respon = self.get_user_actived()
            if  respon.status_code == 200:
                self.page_data['title'] = 'Dashboard'
                self.page_data['description'] = 'Rekapitulasi berkas register'
                self.render('dashboard.html', page=self.page_data, useractived=respon.json()['result'])
        except Exception as e:
        	self.write(e)
