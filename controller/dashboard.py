import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):

    @tornado.web.authenticated
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            self.page_data['title'] = 'Dashboard'
            self.page_data['description'] = 'Rekapitulasi berkas register'
            self.render('page/home/dashboard.html', page=self.page_data, useractived=useractived)
        else:
            self.redirect("/login")
