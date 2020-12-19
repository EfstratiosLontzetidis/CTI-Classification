from serviceDB.mongoDBService import *


def clear_db():
    collections = ["emailAttachment",
                   ]

    for collection in collections:
        col = ClientDB.db[collection]
        col.drop()
