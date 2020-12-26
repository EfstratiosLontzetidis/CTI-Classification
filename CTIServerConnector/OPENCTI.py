from pycti import OpenCTIApiClient
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import stix_to_json
from stix2 import parse
import json, re
from CTIServerConnector.SuperConnector import SuperConnector


class OPENCTI(SuperConnector):

    def __init__(self):
        super().__init__()

    def get_ids(self, data):
        ids = re.findall('(?:"id":\s")(.*\d)', str(data))
        return ids

    # OpenCTI get CTIPs
    def api_con(self):

        # Variables
        api_url = "http://localhost:8080/graphql"
        api_token = "8f8f45a6-769f-4f52-9848-c7ab1e7daa2b"

        # OpenCTI initialization
        opencti_api_client = OpenCTIApiClient(api_url, api_token)


        # Get malwares in STIX2 and place them in database
        data_malwares = opencti_api_client.stix2.export_list("malware")
        # Make the data in json format
        data_malwares_json= json.dumps(data_malwares, indent=4)
        print("Pulling malwares in STIX2")
        #take malware's ids
        malware_ids=self.get_ids(data_malwares_json)
        #loop to get malwares one by one
        for id in malware_ids:
            if "bundle" not in id:
                try:
                    CTIP = json.dumps(opencti_api_client.stix2.export_entity(entity_id=id), indent=4)
                    CTIP_parsed = parse(CTIP, allow_custom=True)
                    Stix2Collection = ClientDB.db["CTIPsToStix2"]
                    Stix2Collection.insert_one(stix_to_json(CTIP_parsed))
                    print("CTIP with id: " + id + " has successfully been added to the database Stix2")
                    print("===================================================================================")
                except Exception:
                    pass

        # Get reports in STIX2 and place them in database
        data_reports = opencti_api_client.stix2.export_list("report")
        # Make the data in json format
        data_reports_json = json.dumps(data_reports, indent=4)
        print("Pulling reports in STIX2")
        # take malware's ids
        reports_ids = self.get_ids(data_reports_json)
        # loop to get malwares one by one
        for id in reports_ids:
            if "bundle" not in id:
                try:
                    CTIP = json.dumps(opencti_api_client.stix2.export_entity(entity_id=id), indent=4)
                    CTIP_parsed = parse(CTIP, allow_custom=True)
                    Stix2Collection = ClientDB.db["CTIPsToStix2"]
                    Stix2Collection.insert_one(stix_to_json(CTIP_parsed))
                    print("CTIP with id: " + id + " has successfully been added to the database Stix2")
                    print("===================================================================================")
                except Exception:
                    pass

