import requests

# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.berkas import BerkasModel


class ComponseController(BaseController):

    def get(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        useractived = self.get_user_actived(cookies=self.get_cookies_user())

        role = self.get_user_role(cookies=self.get_cookies_user(), key="REGIN")
        if role.status_code == 200:

            # load view
            if useractived.status_code == 200:
                self.page_data['title'] = 'Compose'
                self.page_data['description'] = 'Register New Berkas'
                self.render('page/register/compose.html', page=self.page_data, useractived=useractived.json()['result'])
            else:
                self.redirect("/login")
        else:
            self.page_data['title'] = '403'
            self.page_data['description'] = 'Access denied'
            self.render("page/error/403.html", page=self.page_data,  useractived=useractived.json()['result'])


    def post(self):
        # refresh cookies data
        self.refresh_cookies(cookies=self.get_cookies_user())
        cookies = self.get_cookies_user()

        # client request
        body = tornado.escape.json_decode(self.request.body)

        berkas = BerkasModel(officeid=cookies['officeid'], host=options.apis, token=cookies['token'])
        response = berkas.search(nomor=body['nomor'], tahun=body['tahun'])
        if response['status'] == True:
            self.write({'data': response['data']})
        else:
            self.write({'data': []})
