from pymongo import MongoClient
from stix2 import parse

file=open("stix2_indicator.json")
stix2=parse(file)
client = MongoClient('mongodb://localhost:27017/')
db = client['CTIPs']
collection = db['Stix2']
collection1 = db['Review']
collection.insert_one(stix2)