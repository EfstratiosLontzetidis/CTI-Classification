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

        # Database connect and select db,collection, collection->for valid stix2 , collection1->not valid stix2, for review
        client = MongoClient('mongodb://localhost:27017/')
        db = client['CTIPs']
        collection = db['Stix2']
        collection1 = db['Review']

        # Get malwares in STIX2 and place them in database
        data = opencti_api_client.stix2.export_list("malware")
        data = json.dumps(data, indent=4)
        # Place them in a file and validate the STIX2 format
        with open('opencti_stix2_malwares.json', 'w') as outfile:
            json.dump(data, outfile)
        results = validate_file("opencti_stix2_malwares.json")
        if "Error" not in results:
            # if valid stix2 format store them in database for stix2 formats
            collection.insert_many(data)
        else:
            collection1.insert_many(data)

        # Get reports in STIX2 and place them in database
        data = opencti_api_client.stix2.export_list("report")
        data = json.dumps(data, indent=4)
        # Place them in a file and validate the STIX2 format
        with open('opencti_stix2_reports.json', 'w') as outfile:
            json.dump(data, outfile)
        results = validate_file("opencti_stix2_malwares.json")
        if "Error" not in results:
            # if valid stix2 format store them in database for stix2 formats
            collection.insert_many(data)
        else:
            collection1.insert_many(data)
