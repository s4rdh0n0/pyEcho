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
            cookies = self.get_cookies_user()
            dheader = {'Authorization': 'Bearer {}'.format(cookies['token'])}
            respon = requests.get('{}/{}{}'.format(options.apis, 'offices/users/find?username=', cookies['username']), headers=dheader)
            if respon == 200:
                self.render('dashboard.html', user=respon.json()['result'])
        except Exception as e:
        	self.write(e)
