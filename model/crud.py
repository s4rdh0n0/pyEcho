import model.base

class CRUDModel():
    """
    docstring
    """
    
    def __init__(self, collection:None):
        self.collection = collection

    def select(self, filter:{}):
        return self.collection.find(filter)

    def find(self, filter: {}, field: {}):
        if field == {}:
            return self.collection.find_one(filter)
        else:
            return self.collection.find_one(filter, field)

    def count(self, filter: {}):
        return self.collection.count(filter)

    def insert(self, schema: {}):
        return self.collection.insert_one(schema)

    def update(self, filter: {}, schema: {}):
        return self.collection.update_one(filter, schema)

    def delete(self, filter: {}):
        return self.collection.delete_one(filter)

