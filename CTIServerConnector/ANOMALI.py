from taxii2client.v20 import Server,Collection
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import stix_to_json
import json, re,requests
from requests.auth import HTTPBasicAuth
from stix2 import parse
from CTIServerConnector.SuperConnector import SuperConnector

class ANOMALI(SuperConnector):

    def __init__(self):
        super().__init__()

    # Anomali get CTIPs
    def api_con(self):
        Stix2Collection = ClientDB.db["ANOMALI_STIX2"]
        #ids of collections
        ids={"0":"107","1":"135","2":"136","3":"150","4":"200","5":"209","6":"31","7":"313","8":"33","9":"41","10":"68"}
        for x in ids:
            col=Collection("https://limo.anomali.com/api/v1/taxii2/feeds/collections/"+str(ids[str(x)])+"/", user="guest",password="guest")
            collection_json=json.dumps(col.get_objects(),indent=4)
            ctips_parsed = json.loads(collection_json)
            for y in range(len(ctips_parsed['objects'])):
                CTIP = parse(ctips_parsed['objects'][y], allow_custom=True)
                try:
                    Stix2Collection.insert_one(stix_to_json(CTIP))
                    print(CTIP)
                except AttributeError:
                    continue















