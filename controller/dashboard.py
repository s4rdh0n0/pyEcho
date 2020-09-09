import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):

    @tornado.web.authenticated
    def get(self):
        self.refresh_cookies(cookies=self.get_cookies_user())
        response = self.get_user_actived(cookies=self.get_cookies_user())
        if  response.status_code == 200:
            self.page_data['title'] = 'Dashboard'
            self.page_data['description'] = 'Rekapitulasi berkas register'
            self.render('page/home/dashboard.html', page=self.page_data, useractived=response.json()['result'])
