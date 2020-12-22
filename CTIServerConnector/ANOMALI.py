from taxii2client.v20 import Server
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import stix_to_json
import json, re
from stix2 import parse
from CTIServerConnector.SuperConnector import SuperConnector

class ANOMALI(SuperConnector):

    def __init__(self):
        super().__init__()

    def get_ids(self, collection):
        ids = re.findall('(?:"id":\s")(.*\d)', str(collection))
        return ids


    # OpenCTI get CTIPs
    def api_con(self):

        server = Server("https://cti-taxii.mitre.org/taxii/")

        api_root = server.api_roots[0]

        server = Server("https://limo.anomali.com/api/v1/taxii2/feeds/", user="guest", password="guest")
        #loop to get collection by collection id
        for x in range(len(api_root.collections)):
            print("Starting collection number: "+str(x))
            collection = api_root.collections[x]
            #make the collection in json format
            collection_json= json.dumps(collection.get_objects(), indent=4)
            #take the collection's ids
            collection_ids=self.get_ids(collection_json)
            #loop in order to get CTIPs one by one
            for id in collection_ids:
                if "bundle" not in id:
                    #auto pull CTIP with id taken from the method
                    try:
                        CTIP=json.dumps(collection.get_object(obj_id=id),indent=4)
                        CTIP_parsed=parse(CTIP, allow_custom=True)
                        Stix2Collection=ClientDB.db["CTIPsToStix2"]
                        Stix2Collection.insert_one(stix_to_json(CTIP_parsed))
                        print("CTIP with id: "+id+" has successfully been added to the database Stix2")
                        print("===================================================================================")
                    except Exception:
                        pass










