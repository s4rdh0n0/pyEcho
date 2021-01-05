import requests

from model.base import BaseModel


class RegisterModel(BaseModel):

    root = 'offices/register'

    schema = {
        '_id': None,
        'nomorregister': None,
        'createregisterdate': None,
        'finnishregisterdate': None,
        'pegawaiactived': None,
        'nodeactived': None,
        'officeid': None,
        'officetype': None,
        'officenama': None,
        'kecamatanid': None,
        'kecamatancode': None,
        'namakecamatan': None,
        'desaid': None,
        'desacode': None,
        'namadesa': None,
        'berkasid': None,
        'nomorberkas': None,
        'tahunberkas': None,
        'prosedur': None,
        'kegiatan': None,
        'phone': None,
        'email': None,
        'startdate': None,
        'pemilik': [],
        'node': [],
        'keterangan': None,
        'status': None,
        'actived': False
    }

    schema_node = {
        '_id': None,
        'node': None,
        'sender': None,
        'sentdate': None,
        'messange': None,
        'operator': None,
        'startdate': None,
        'actived': False,
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

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

