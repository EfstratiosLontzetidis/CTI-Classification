from pycti import OpenCTIApiClient, OpenCTIStix2
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
        #custom_attributes = """
            #id
            #name
            #published
            #description
        #"""
        #data = opencti_api_client.report.list(
               #customAttributes=custom_attributes,
        #)
        data = opencti_api_client.stix2.export_list("report")

        return json.dumps(data, indent=4)
