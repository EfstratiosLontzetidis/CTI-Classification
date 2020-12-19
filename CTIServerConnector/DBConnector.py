from pymongo import MongoClient

class DBConnector(object):

    def __init__(self):
        #create the connection,take the db and collections
        self.client= MongoClient('mongodb://localhost:27017/')
        self.db = self.client['CTIPs']
        self.collection_stix2 = self.db['Stix2']
        self.collection_other = self.db['Review']

    def insert_stix2_to_db(self, stix2_object):
        #insert stix2 to db
        self.collection_stix2.insert_many(stix2_object)

    def insert_other_to_db(self, json_object):
        #insert other format to db
        self.collection_other.insert_many(json_object)