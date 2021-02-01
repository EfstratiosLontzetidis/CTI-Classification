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
        # not tested yet because of opencti client is slow

        # Variables
        api_url = "http://localhost:8080/graphql"
        api_token = "8f8f45a6-769f-4f52-9848-c7ab1e7daa2b"

        # OpenCTI initialization
        opencti_api_client = OpenCTIApiClient(api_url, api_token)

        #get ready database
        Stix2Collection = ClientDB.db["CTIPsToStix2"]


        # Get malwares in STIX2 and place them in database
        try:
            data_malwares = opencti_api_client.stix2.export_list("malware")
            # Make the data in json format
            data_malwares_json= json.dumps(data_malwares, indent=4)
            data_malwares_json_parsed=json.loads(data_malwares_json)
            for x in range(len(data_malwares_json_parsed['objects'])):
                malware=data_malwares_json_parsed['objects'][x]
                print(malware)
                malware_parsed=parse(malware,allow_custom=True)
                Stix2Collection.insert_one(stix_to_json(malware_parsed))
        except Exception:
            print("OpenCTI Error for malwares")

        # Get reports in STIX2 and place them in database
        try:
            data_reports = opencti_api_client.stix2.export_list("report")
            # Make the data in json format
            data_reports_json = json.dumps(data_reports, indent=4)
            data_reports_json_parsed = json.loads(data_reports_json)
            for x in range(len(data_reports_json_parsed['objects'])):
                report = data_reports_json_parsed['objects'][x]
                print(report)
                report_parsed = parse(report, allow_custom=True)
                Stix2Collection.insert_one(stix_to_json(report_parsed))
        except Exception:
            print("OpenCTI Error for reports")


