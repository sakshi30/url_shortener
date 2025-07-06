from pymongo import MongoClient
import os

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URL"))
        self.database = self.client[os.getenv("MONGO_DB")]
        print("Database connection successful")

    def insert_document(self, document, collection):
        collection = self.database[collection]
        inserted = collection.insert_one(document)
        return inserted

    def get_document(self, document, collection):
        collection = self.database[collection]
        response = collection.find_one(document)
        return response


