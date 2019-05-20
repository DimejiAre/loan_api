from pymongo import MongoClient


class Database(object):

    database = None

    @staticmethod
    def initialize():
        client = MongoClient()
        Database.database = client.LoanShark

    @staticmethod
    def insert(collection, data):
        Database.database[collection].insert(data)

    @staticmethod
    def find(collection):
        return Database.database[collection].find()

    @staticmethod
    def find_one(collection, query):
        return Database.database[collection].find_one(query)

    @staticmethod
    def delete(collection, query):
        Database.database[collection].delete_one(query)

    @staticmethod
    def update(collection, match, data):
        Database.database[collection].update_one(match, data)
