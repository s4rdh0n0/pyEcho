from datetime import date, datetime, timedelta
import arrow


# Tornado Framework
import tornado.web
from tornado.options import options

# Controller
from controller.base import BaseController

# Model
from model.berkas import BerkasModel
from model.user import UserModel
from model.register import RegisterModel
from model.ndl_persil import NDLPersilModel


class DashboardController(BaseController):

	def initialize(self):
		self.useractived = None

	@tornado.web.authenticated
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		try:
			berkas = BerkasModel(collection=self.CONNECTION.collection(database="pyDatabase", name="berkas"), service=None)
			register = RegisterModel(collection=self.CONNECTION.collection(database="pyDatabase", name="register"), service=None)
			petugas = UserModel(collection=self.CONNECTION.collection(database="pyDatabase", name="users"), service=None)


			week_now = arrow.now()
			start_of_week = week_now.floor('week')
			end_of_week = week_now.ceil('week')

			today = date.today()
			start = datetime(
				year=today.year,
				month=today.month,
				day=today.day,
			)
			end = datetime.now()
			schema_berkas = {
				'masuk': berkas.count(filter={"officeid": self.get_cookies_user()['officeid']}),
				'masuk_harini': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'userregisterindate': {'$gte': start, '$lt': end}}),
				'proses': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'PROSES', 'actived': True}),
				'tunda': berkas.count(filter={'officeid': self.get_cookies_user()['officeid'], 'status': 'TUNDA', 'actived': True}),
				'selesai': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False}),
                'selesai_hariini': berkas.count(filter={"officeid": self.get_cookies_user()['officeid'], 'status': 'FINNISH', 'actived': False, 'finnishdate': {'$gte': start, '$lt': end}})
			}
			call_berkas = []
			index = 1
			for p in petugas.select(filter={'officeid': self.useractived['officeid']}):
				p['index'] = index
				p['start_week'] = datetime(year=start_of_week.year,month=start_of_week.month,day=start_of_week.day)
				p['end_week'] = datetime(year=end_of_week.year,month=end_of_week.month,day=end_of_week.day)
				p['tunggakan'] = register.count({'recieve': p['_id'], 'actived': True})
				p['tunggakan_minggu_ini'] = register.count({'recieve': p['_id'], 'senderdate': {'$gte': datetime(year=start_of_week.year,month=start_of_week.month,day=start_of_week.day), '$lt': datetime(year=end_of_week.year,month=end_of_week.month,day=end_of_week.day)}, 'actived': True})
				p['tunggakan_lebih_seminggu'] = p['tunggakan'] - p['tunggakan_minggu_ini']
				p['tunggakan_sdh_diterima'] = register.count({'recieve': p['_id'], 'recievedate':{'$ne': None }, 'actived': True})
				p['selesai'] = register.count({'recieve': p['_id'], 'actived': False})
				p['selesai_minggu_ini'] = register.count({'recieve': p['_id'], 'senderdate': {'$gte': datetime(year=start_of_week.year,month=start_of_week.month,day=start_of_week.day), '$lt': datetime(year=end_of_week.year,month=end_of_week.month,day=end_of_week.day)}, 'actived': False})
				index = index + 1
				call_berkas.append(p)

			self.page_data['title'] = 'Dashboard'
			self.page_data['menu'] = 'dashboard'
			self.page_data['description'] = 'Rekapitulasi register berkas'
			self.render('page/home/dashboard.html', 
						page=self.page_data, 
						useractived=self.useractived,
						berkas=schema_berkas,
						call_berkas=call_berkas)

		except Exception as e:
			print(e)


class NDLPersilController(BaseController):

	def initialize(self):
		self.useractived = None

	@tornado.web.authenticated
	def get(self):
		self.useractived = self.get_user_actived(cookies=self.get_cookies_user())
		ndl = NDLPersilModel(collection=self.CONNECTION.collection(database="pyDatabase", name="ndl_persil"), service=None)
		try:
			table = []
			index = 1
			for n in ndl.select(filter=None):
				n['row'] = index
				table.append(n)
				index = index + 1


			self.page_data['title'] = 'NILAI DESA LENGKAP (PERSIL)'
			self.page_data['menu'] = 'ndl persil'
			self.page_data['description'] = 'PERBANDINGAN LUAS DESA DAN LUAS BIDANG TANAH'
			self.render('page/home/ndl_persil.html',
                            page=self.page_data,
                            useractived=self.useractived,
                            ndl=table)
		except Exception as e:
			print(e)

