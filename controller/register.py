import requests
import datetime
from bson import json_util
import json
import uuid


# Tornado Framework
import tornado.gen
import tornado.escape
from tornado.options import options
from tornado import gen

# Controller
from controller.base import BaseController

# Model
from model.region import RegionModel
from model.office import OfficeModel
from model.user import UserModel
from model.berkas import BerkasModel
from model.region import RegionModel
from model.master import MasterModel
from model.inbox import InboxModel
from model.node import NodeModel

class InboxController(BaseController):

    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            if len(useractived['role']) != 0 and useractived['actived']:
                self.page_data['title'] = 'Inbox'
                self.page_data['description'] = 'Inbox Register Berkas'
                self.render('page/register/inbox.html', page=self.page_data, useractived=useractived)

            else:
                self.page_data['title'] = '403'
                self.page_data['description'] = 'Access denied'
                self.render("page/error/403.html", page=self.page_data,  useractived=useractived)
        else:
            self.redirect("/logout")

    
    def post(self):
        useractived = self.get_user_actived(cookies=self.get_cookies_user())
        if useractived != None:
            # client request
            cookies = self.get_cookies_user()
            body = tornado.escape.json_decode(self.request.body)

            list_response = []
            count_reponse = 0

            node  = self.CONNECTION.collection(database="1228_trenggalek", name="node")
            register = InboxModel(collection=self.CONNECTION.collection(database="1228_trenggalek", name="inbox"), node=node, service=None)


            count_reponse = register.count(filter={"officeid": cookies['officeid'] ,"pegawaiactived": cookies['userid']})
            list_response  = register.pagination(filter={"officeid": cookies['officeid'] ,"pegawaiactived": cookies['userid']},page_size=count_reponse, page_num=body['page'] + 1)

            self.write({'status': True, 'draw': body['draw'], 'data': json.dumps(list_response, default=json_util.default), 'recordsTotal': count_reponse, 'recordsFiltered': count_reponse})
        else:
            self.redirect("/logout")
