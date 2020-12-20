from pymongo import MongoClient


class ClientDB:
    client = MongoClient("mongodb://localhost:27017/")
    db1 = client["CTIPsToStix2"]
    db2 = client["CTIPsToJson"]
