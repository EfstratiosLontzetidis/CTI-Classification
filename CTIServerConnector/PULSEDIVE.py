#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
from CTIServerConnector.SuperConnector import SuperConnector


class PULSEDIVE(SuperConnector):

    def __init__(self):
        super().__init__()

    # IBM get CTIPs
    def api_con(self):
        #results by id,can make a loop to take each one, problem when threat not found**
        response = requests.get("https://pulsedive.com/api/info.php?tid=1&pretty=1&key=ccb008a66b43702e60bf2606826272f1a18730d718070383bb4beb17b7b6c31b")
        return json.dumps(response.json(), indent=4, sort_keys=True)
