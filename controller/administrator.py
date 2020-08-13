# Tornado Framework
import tornado.web

# Controller
from controller.base import BaseController


class DaftarPegawaiController(BaseController):


    @tornado.web.authenticated
    def get(self):
        self.refresh_cookies()
        try:
            respon = self.get_user_actived()
            if  respon.status_code == 200:
                self.page_data['title'] = 'Daftar Pegawai'
                self.page_data['description'] = 'Rekapituasi berkas register'
                self.render('administrator/daftarpegawai.html', page=self.page_data, useractived=respon.json()['result'])
        except Exception as e:
        	self.write(e)