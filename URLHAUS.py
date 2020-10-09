#!/usr/bin/env python

import requests
import json
from CTIP import CTIP


class URLHAUS(CTIP):
    pass

    def __init__(self):
        super().__init__()
        self.data = []


    # URLhaus API connect
    def api_con(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        return json.dumps(response.json(), indent=4, sort_keys=True)
