import model.base



class CRUDModel():
    """
    docstring
    """
    
    def __init__(self, collection:None):
        self.collection = collection

    def pagination(self, page_size:int, page_num:int):
        skips = page_size * (page_num - 1)
        cursor = self.collection.find().skip(skips).limit(page_size)

        return [x for x in cursor]

    def find(self, filter:{}, field:{}):
        if field == {}:
            return self.collection.find_one(filter)
        else:
            return self.collection.find_one(filter, field)

    def count(self, filter:{}):
        return self.collection.count(filter)

    def insert(self, schema:{}):
        return self.collection.insert_one(schema)

    def update(self, filter:{}, schema:{}):
        return self.collection.update_one(filter, schema)

    def delete(self, filter:{}):
        return self.collection.delete_one(filter)

