#!/usr/bin/env python

import requests
import json

from CTIServerConnector.SuperConnector import SuperConnector


class URLHAUS(SuperConnector):

    def __init__(self):
        super().__init__()

    # URLhaus get CTIPs
    def api_con(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        return json.dumps(response.json(), indent=4, sort_keys=True)
