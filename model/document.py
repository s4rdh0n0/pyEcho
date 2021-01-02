import requests

# Model
from model.base import BaseModel


class PersilModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    
    def pagination(self, officeid:str, nib:str, draw:str, start:str, limit:str):
        response = requests.get('{}/offices/document/persil'.format(self.host), params={"officeid": officeid, "nib": nib, "start": start, "limit": limit, "count": -1})

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, persilid:str):
        return requests.get('{}/offices/document/persil/find'.format(self.host), params={"persilid": persilid})

class SuratUkurModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, typesu:str, nomor:str, tahun:str, draw:str, start:str, limit:str):
        response = requests.get('{}/offices/document/suratukur'.format(self.host), params={"officeid": officeid, "desaid": desaid, "typesu": typesu, "nomor":nomor, "tahun": tahun, "start": start, "limit": limit, "count": -1})

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, suratukurid:str):
        param = 'suratukurid={}'.format(suratukurid)
        return requests.get('{}/{}/find?{}'.format(self.host, self.root, param), params={"suratukurid": suratukurid})

class BukuTanahModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, typehak:str, nomor:str, draw:str, start:str, limit:str):
        response = requests.get('{}/offices/document/bukutanah'.format(self.host), params={"officeid": officeid, "desaid": desaid, "typehak": typesu, "nomor":nomor, "start": start, "limit": limit, "count": -1})

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, bukutanahid:str):
        return requests.get('{}/offices/document/bukutanah/find'.format(self.host, self.root, param), params={"bukutanahid": bukutanahid})

class GambarUkurModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def pagination(self, nomor:str, tahun:str, draw:str, start:str, limit:str):
        response = requests.get('{}/offices/document/gambarukur'.format(self.host), params={"officeid": officeid, "nomor":nomor, "tahun": tahun, "start": start, "limit": limit, "count": -1})

        if response.status_code == 200:
            return {'status': True, 'draw': draw, 'data': response.json()['result'], 'recordsTotal': response.json()['count'], 'recordsFiltered': response.json()['count']}
        else:
            return {'status': True, 'draw': draw, 'data': [], 'recordsTotal': 0, 'recordsFiltered': 0}

    def find(self, dokumenpengukuranid:str):
        return requests.get('{}//offices/document/gambarukur/find'.format(self.host), params={"dokumenpengukuranid": dokumenpengukuranid})

class STPModel(BaseModel):

    def __init__(self, collection: None, service: None):
        super().__init__(collection=collection, service=service)

    def find(self, stpid:str):
        return requests.get('{}/offices/document/stp/find'.format(self.host, self.root, param), headers={"stpid": stpid})
