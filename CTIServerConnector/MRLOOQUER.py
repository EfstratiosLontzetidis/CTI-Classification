#!/usr/bin/env python

import requests
import json
from stix2 import parse, Indicator
from CTIServerConnector.SuperConnector import SuperConnector


class MRLOOQUER(SuperConnector):

    def __init__(self):
        super().__init__()

    # MRLOOQUER get CTIPs,csv ,not one by one
    def api_con(self):
        response = requests.get("https://iocfeed.mrlooquer.com/feed.json")
        #parse the converted json
        parse=json.loads(json.dumps(response.json(), indent=4))
        for x in range(len(parse)):
            print(parse[x]['domain'])
        #return json.dumps(response.json(), indent=4)
