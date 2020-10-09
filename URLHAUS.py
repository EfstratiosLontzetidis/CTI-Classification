#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
from CTIP import CTIP


class URLHAUS(CTIP):
    pass

    def __init__(self):
        self.data = []


    # URLhaus API connect
    def urlhaus_api(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        return json.dumps(response.json(), indent=4, sort_keys=True)
