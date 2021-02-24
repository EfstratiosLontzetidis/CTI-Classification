#!/usr/bin/env python
import requests, json
from CTIServerConnector.SuperConnector import SuperConnector
from stix2 import Report,parse
from Utilities.utility import stix_to_json
from serviceDB.mongoDBService import ClientDB


class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()

    def convert_ctips_to_stix2(self,response):
        x = json.loads(response.content.decode())
        ctips = json.dumps(x, indent=4)
        ctips_parsed = json.loads(ctips)
        for i in range(len(ctips_parsed)):
            print(json.dumps(ctips_parsed[1], indent=4))
            break

    # Blueliv get CTIPs
    def api_con(self):
        headers = {'Authorization':'Token c1ddf06a-5895-4ba0-a5bc-025f8caba1e9'}
        response = requests.get("https://community.blueliv.com/api/v1/tags/API/sparks", headers=headers)
        self.convert_ctips_to_stix2(response)


