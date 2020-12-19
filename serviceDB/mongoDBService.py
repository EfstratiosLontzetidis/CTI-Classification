from pymongo import MongoClient


class ClientDB:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CTIClassification"]
