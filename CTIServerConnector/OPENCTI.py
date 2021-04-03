from pycti import OpenCTIApiClient
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import stix_to_json
from stix2 import parse
import json
from CTIServerConnector.SuperConnector import SuperConnector


class OPENCTI(SuperConnector):

    def __init__(self):
        super().__init__()


    # OpenCTI get CTIPs
    def api_con(self):

        # Variables
        api_url = "http://localhost:8080/graphql"
        api_token = "8f8f45a6-769f-4f52-9848-c7ab1e7daa2b"

        # OpenCTI initialization
        opencti_api_client = OpenCTIApiClient(api_url, api_token)

        # get ready database
        Stix2Collection = ClientDB.db["OPENCTI_STIX2"]


        types = ["malware", "intrusion-set", "marking-definition", "indicator", "relationship", "tool", "vulnerability",
                 "infrastructure", "identity", "course-of-action", "attack-pattern", "sighting", "campaign",
                 "threat-actor", "observed-data", "report"]
        for x in types:
            try:
                data = opencti_api_client.stix2.export_list(x)
                data_json = json.dumps(data, indent=4)
                data_json_parsed = json.loads(data_json)
                for y in range(len(data_json_parsed['objects'])):
                    stix2_data = data_json_parsed['objects'][y]
                    if (stix2_data['external_references']) is not None:
                        del stix2_data['external_references']
#                         for w in range(len(stix2_data['external_references'])):
#                             del stix2_data['external_references'][w]['id']
#                             del stix2_data['external_references'][w]['x_opencti_id']
#                             del stix2_data['external_references'][w]['x_opencti_created']
#                             del stix2_data['external_references'][w]['x_opencti_modified']
                    print(stix2_data)
                    stix2_data_parsed = parse(stix2_data, allow_custom=True)
                    Stix2Collection.insert_one(stix_to_json(stix2_data_parsed))
            except Exception:
                continue

