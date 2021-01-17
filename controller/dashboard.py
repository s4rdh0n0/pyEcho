import requests

# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController


class DashboardController(BaseController):

    @tornado.web.authenticated
    def get(self):
        _connection = self.CONNECTION
        with _connection.client.start_session() as session:
            try:
                useractived = self.get_user_actived(cookies=self.get_cookies_user(), session=session)
                if useractived['actived']:
                    self.page_data['title'] = 'Dashboard'
                    self.page_data['description'] = 'Rekapitulasi berkas register'
                    self.render('page/home/dashboard.html', page=self.page_data, useractived=useractived)
                else:
                    self.redirect("/logout")
            except Exception as e:
                self.redirect("/logout")
