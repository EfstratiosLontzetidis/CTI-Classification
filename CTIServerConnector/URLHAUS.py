#!/usr/bin/env python

import requests
import json

from CTIServerConnector.SuperConnector import SuperConnector


class URLHAUS(SuperConnector):

    def __init__(self):
        super().__init__()

    def payloads_to_stix2(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        for x in range(len(parsed_CTIPs['payloads'])):
            print(parsed_CTIPs['payloads'][x]['file_size'])
            break

    def urls_to_stix2(self):
        response=requests.get("https://urlhaus-api.abuse.ch/v1/urls/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        for x in range(len(parsed_CTIPs['urls'])):
            print(parsed_CTIPs['urls'][x]['id'])
            break


    # URLhaus get CTIPs
    def api_con(self):
        self.payloads_to_stix2()
        self.urls_to_stix2()
