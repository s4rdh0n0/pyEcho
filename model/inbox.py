import requests

from model.base import BaseModel


class InboxModel(BaseModel):

    root = 'offices/register'

    schema = {
        '_id': None,
        'officeid': None,
        'officetype': None,
        'officenama': None,
        'kecamatanid': None,
        'kecamatancode': None,
        'namakecamatan': None,
        'desaid': None,
        'desacode': None,
        'namadesa': None,
        'nomorberkas': None,
        'tahunberkas': None,
        'prosedur': None,
        'kegiatan': None,
        'phone': None,
        'email': None,
        'startdate': None,
        'pemilik': [],
        'daftarisian': [],
        'document': [],
        'keterangan': None,
        'pegawaiactived': None,
        'nodeactived': None,
        'status': None,
        'actived': False
    }

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, filter:{}, page_size:int, page_num:int):
        skips = page_size * (page_num - 1)
        cursor = self.collection.find(filter).skip(skips).limit(page_size)

        return [x for x in cursor]