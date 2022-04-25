from db.mongo_access import Document, db


class User(Document):
    collection = db.users
