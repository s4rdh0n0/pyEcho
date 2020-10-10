import requests

from model.base import BaseModel


class RegisterModel(BaseModel):

    root = 'offices/register'

    schema = {
        '_id': None,
        'nomorregister': None,
        'pegawaiactived': None,
        'officeid': None,
        'kecamatanid': None,
        'namakecamatan': None,
        'desaid': None,
        'namadesa': None,
        'typealashak': None,
        'nomoralashak': None,
        'nomorberkas': None,
        'tahunberkas': None,
        'spopp': None,
        'prosedur': None,
        'kegiatan': None,
        'createdate': None,
        'finnishdate': None,
        'pemohon': [],
        'node': [],
        'document': [],
        'status': None,
    }

    schema_node = {
        'nodeid':None,
        'sender': None,
        'senderdate': None,
        'sendermessange': None,
        'receiver': None,
        'receiverdate': None,
        'selesai': False,
    }

    schema_pemilik = {
        'pemilikberkasid': None,
        'kantorid': None,
        'berkasid': None,
        'pemilikid': None,
        'tipepemilikid': None,
        'nomoridentitas': None,
        'nik': None,
        'gelardepan':None,
        'nama': None,
        'gelarbelakang': None,
        'jeniskelamin': None,
        'tempatlahir': None,
        'tanggallahir': None,
        'alamat': None,
    }

    schema_alashak = {
        'typealashakid': None,
        'alashakid': None,
        'nomor': None,
    }

    schema_document = {
        'typedocumentid': None,
        'documentid': None,
        'nomor': None,
    }

    def __init__(self, officeid="", host="", token=""):
        self.officeid = officeid
        super().__init__(host=host, token=token)


    def pagination(self, pegawaiid="", nomor="", tahun="", status="", draw=0, page=0, limit=0, start=0):
        record = self.count(pegawaiid=pegawaiid, nomor=nomor, tahun=tahun, status=status)
        if record.status_code == 200:
            param = 'officeid={}&pegawaiid={}&nomorberkas={}&tahunberkas={}&status={}'.format(self.host, pegawaiid, nomor, tahun, status)
            register = requests.get('{}/{}?{}'.format(self.host, self.root, param), headers=self.header)
            if register.status_code == 200:
                if register.json()['result'] != None:
                    return {'status': True, 'draw': draw, 'data': register.json()['result'], 'recordsTotal': record.json()['result'], 'recordsFiltered': record.json()['result']}
                else:
                    return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}
            else:
                return {'status': False, 'draw': 0, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def count(self, pegawaiid="", nomor="", tahun="", status=""):
        param = 'officeid={}&pegwaiid={}&nomorberkas={}&tahunberkas={}&status={}'.format(self.host, pegawaiid, nomor, tahun, status)
        return requests.get('{}/{}/count?{}'.format(self.host, self.token, param), headers=self.header)

    def find(self, typeid="", registerid=""):
        param = 'typeid={}&registerid={}'.format(typeid, registerid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), headers=self.header)

    def add(self, register={}):
        djson = {
            'register': register
        }
        return requests.post('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def update(self, register={}):
        djson = {
            'register': register
        }
        return requests.put('{}/{}'.format(self.host, self.root), json=djson, headers=self.header)

    def delete(self, typeid="", registerid=""):
        djson = {
            'typeid': typeid,
            'registerid': registerid,
        }
        return requests.delete('{}/{}'.format(self.host, self.root, json=djson, headers=self.header))

    