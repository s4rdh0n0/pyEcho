import model.base

class CRUDModel():
    """
    docstring
    """
    
    def __init__(self, collection:None):
        self.collection = collection

    def select(self, filter:{}, session: None):
        return self.collection.find(filter, session=session)

    def find(self, filter: {}, field: {}, session: None):
        if field == {}:
            return self.collection.find_one(filter, session=session)
        else:
            return self.collection.find_one(filter, field, session=session)

    def count(self, filter: {}, session: None):
        return self.collection.count(filter, session=session)

    def insert(self, schema: {}, session: None):
        return self.collection.insert_one(schema, session=session)

    def update(self, filter: {}, schema: {}, session: None):
        return self.collection.update_one(filter, schema, session=session)

    def delete(self, filter: {}, session: None):
        return self.collection.delete_one(filter, session=session)

