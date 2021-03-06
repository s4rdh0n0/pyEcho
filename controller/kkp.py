# Tornado Framework
import tornado.gen
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.berkas import BerkasModel
from model.user import UserModel


class BerkasKKPController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def put(self):
		try:
			body = tornado.escape.json_decode(self.request.body)
			berkas =  BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=options.service)

			msg = ""
			status = False
			tipe = ""
			title = ""

			berkas_entity = berkas.find(berkasid=body['berkasid']).json()['result']
			di_entity = berkas.daftarisian(berkasid=body['berkasid']).json()['result']
			doc_entity = berkas.produk(berkasid=body['berkasid']).json()['result']

			schema_berkas = berkas.get(filter={'_id': body['berkasid']})
			schema_berkas['pemilik'] = berkas_entity['pemohon']
			schema_berkas['daftarisian'] = di_entity
			schema_berkas['document'] = doc_entity
			berkas.update(filter={'_id': body['berkasid']}, schema=schema_berkas)

			msg = "Berkas {}/{} berhasil update data.".format(schema_berkas['nomorberkas'], schema_berkas['tahunberkas'])
			status = True
			tipe = "info"
			title = '<strong>Info</strong> <br>'

			self.write({'status': status, 'title': title, 'type': tipe, 'msg': msg})
		except Exception as e:
			print(e)

class PegawaiKKPController(BaseController):

	@tornado.web.authenticated
	@tornado.gen.coroutine
	def get(self, username=""):
		try:
			response_pegawai = UserModel(collection=None, service=options.service).kkp(officeid=self.get_cookies_user()['officeid'], username=username)
			if response_pegawai.status_code == 200:
				self.write({'status': True, 'data': response_pegawai.json()['result']})
			else:
				self.write({'status': False, 'data': None})
		except Exception as e:
			print(e)
