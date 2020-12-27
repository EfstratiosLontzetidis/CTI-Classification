#!/usr/bin/env python

import requests
import json

from CTIServerConnector.SuperConnector import SuperConnector


class URLHAUS(SuperConnector):

    def __init__(self):
        super().__init__()

    # URLhaus get CTIPs
    def api_con(self):
        #response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/limit/1")
        #one by one, need to make regex for taking each md5_hash
        data={'md5_hash': '12c8aec5766ac3e6f26f2505e2f4a8f2'}
        response=requests.post(url="https://urlhaus-api.abuse.ch/v1/payload/", data=data)
        return json.dumps(response.json(), indent=4, sort_keys=True)
