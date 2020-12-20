from taxii2client.v20 import Server
import json, re
from stix2validator import validate_file,print_results
from stix2 import parse
from CTIServerConnector.SuperConnector import SuperConnector

class ANOMALI(SuperConnector):

    def __init__(self):
        super().__init__()

    def get_and_store_stix2(self, collection):
        ids = re.findall('(?:"id":\s)(.*\d")', str(collection))
        return ids


    # OpenCTI get CTIPs
    def api_con(self):

        server = Server("https://cti-taxii.mitre.org/taxii/")

        api_root = server.api_roots[0]

        server = Server("https://limo.anomali.com/api/v1/taxii2/feeds/", user="guest", password="guest")
        #get collection
        collection = api_root.collections[1]
        #make the collection in json format
        collection_json= json.dumps(collection.get_objects(), indent=4)
        #take the collection's ids
        collection_ids=self.get_and_store_stix2(collection_json)
        #manual print of id is working
        #print(collection.get_object(obj_id="relationship--980656e3-ba60-49ee-9ce8-cbe1a0dc65c5"))
        for id in collection_ids:
            if "bundle" not in id:
                #print id
                print(id)
                #auto print with id taken from the method is not working
                print(collection.get_object(obj_id=id))
                print("==================================================")






        #return json.dumps(collection.get_object(obj_id="attack-pattern--784ff1bc-1483-41fe-a172-4cd9ae25c06b"), indent=4)



