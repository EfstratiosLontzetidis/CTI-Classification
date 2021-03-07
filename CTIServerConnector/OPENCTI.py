from pycti import OpenCTIApiClient
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import stix_to_json
from stix2 import parse
import json
from CTIServerConnector.SuperConnector import SuperConnector


class OPENCTI(SuperConnector):

    def __init__(self):
        super().__init__()

    def insert_to_db(self, data):
        Stix2Collection = ClientDB.db["OPENCTI_STIX2"]
        data_json = json.dumps(data, indent=4)
        data_json_parsed = json.loads(data_json)
        for y in range(len(data_json_parsed['objects'])):
            stix2_data = data_json_parsed['objects'][y]
            print(stix2_data)
            stix2_data_parsed = parse(stix2_data, allow_custom=True)
            Stix2Collection.insert_one(stix_to_json(stix2_data_parsed))

    # OpenCTI get CTIPs
    def api_con(self):

        # Variables
        api_url = "http://localhost:8080/graphql"
        api_token = "df8635b1-39b5-41c2-8873-2f19b0e6ca8c"

        # OpenCTI initialization
        opencti_api_client = OpenCTIApiClient(api_url, api_token)

        # get ready database
        Stix2Collection = ClientDB.db["OPENCTI_STIX2"]

        # 1st way to try
        types = ["malware", "intrusion-set", "marking-definition", "indicator", "relationship", "tool", "vulnerability",
                 "infrastructure", "identity", "course-of-action", "attack-pattern", "sighting", "campaign",
                 "threat-actor", "observed-data", "report"]
        for x in types:
            # try:
            data = opencti_api_client.stix2.export_list(x)
            data_json = json.dumps(data, indent=4)
            print(data_json)

            data_json_parsed = json.loads(data_json)
            for y in range(len(data_json_parsed['objects'])):
                stix2_data = data_json_parsed['objects'][y]
                stix2_data_parsed = parse(stix2_data, allow_custom=True)
                Stix2Collection.insert_one(stix_to_json(stix2_data_parsed))
            # except Exception:
            #     continue

        # # 2nd way to try
        # try:
        #     malwares = opencti_api_client.malware.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     identities = opencti_api_client.identity.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     report = opencti_api_client.report.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     indicator = opencti_api_client.indicator.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     attack_pattern = opencti_api_client.attack_pattern.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     campaign = opencti_api_client.campaign.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     course_of_action = opencti_api_client.course_of_action.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     intrusion_set = opencti_api_client.intrusion_set.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     tool = opencti_api_client.tool.to_stix2()
        # except Exception:
        #     print("failed")
        # try:
        #     threat_actor = opencti_api_client.threat_actor.to_stix2()
        # except Exception:
        #     print("failed")
