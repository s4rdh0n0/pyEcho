import requests

from model.base import BaseModel


class RegisterModel(BaseModel):

    root = 'offices/register'

    schema = {
        '_id': None,
        'nomorregister': None,
        'pegawaiactived': None,
        'nodeactived': None,
        'officeid': None,
        'officenama': None,
        'officetype': None,
        'kecamatanid': None,
        'kecamatancode': None,
        'namakecamatan': None,
        'desaid': None,
        'desacode': None
        'namadesa': None,
        'nomorberkas': None,
        'tahunberkas': None,
        'spopp': None,
        'prosedur': None,
        'kegiatan': None,
        'createdate': None,
        'updatedate': None,
        'finnishdate': None,
        'pemohon': [],
        'node': [],
        'document': [],
        'keterangan': None,
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

    schema_document = {
        'documentid': None,
        'typedocument': None,
        'nomor': None,
    }

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

