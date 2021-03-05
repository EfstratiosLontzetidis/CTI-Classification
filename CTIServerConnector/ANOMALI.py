from taxii2client.v21 import Server,Collection
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
        ids={"0":"107","1":"135","2":"136","3":"150","4":"200","5":"209","6":"31","7":"313","8":"33","9":"41","10":"68"}
        # for x in ids:
        #     col=Collection("https://limo.anomali.com/api/v1/taxii2/feeds/collection/"+str(ids[str(x)])+"/", user="guest",password="guest")
        #     col.description
        #     break
        col = Collection("https://limo.anomali.com/api/v1/taxii2/feeds/collection/135/",user="guest", password="guest",verify=False)
        print(col.get_objects())
        #print("https://limo.anomali.com/api/v1/taxii2/feeds/collection/"+str(ids[str(0)]))














