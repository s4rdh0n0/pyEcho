import requests

from model.base import BaseModel


class RegisterModel(BaseModel):

    root = 'offices/register'

    schema = {
        '_id': None,
        'nomorregister': None,
        'pegawaiactived': None,
        'officeid': None,
        'officenama': None,
        'officetype': None,
        'kecamatanid': None,
        'kecamatancode': None,
        'namakecamatan': None,
        'desaid': None,
        'desacode': None
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
        'actived': False
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

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

