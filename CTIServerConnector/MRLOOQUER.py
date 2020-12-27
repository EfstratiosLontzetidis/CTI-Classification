#!/usr/bin/env python

import requests
import json
from CTIServerConnector.SuperConnector import SuperConnector


class MRLOOQUER(SuperConnector):

    def __init__(self):
        super().__init__()

    # MRLOOQUER get CTIPs,csv ,not one by one
    def api_con(self):
        response = requests.get("https://iocfeed.mrlooquer.com/feed.json")
        return json.dumps(response.json(), indent=4)
