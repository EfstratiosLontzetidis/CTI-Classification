from pycti import OpenCTIApiClient
from pymongo import MongoClient
from stix2validator import validate_file
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

        #malware,report,attack-pattern
        # Get malwares in STIX2 and place them in database
        #data = opencti_api_client.stix2.export_list("malware")
        #return json.dumps(data, indent=4)



        # Get reports in STIX2 and place them in database
        #data = opencti_api_client.stix2.export_list("report")
        #data = json.dumps(data, indent=4)

