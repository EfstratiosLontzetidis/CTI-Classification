#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
from CTIP import CTIP


class IBM(CTIP):
    pass

    def __init__(self):
        self.data = []

    # IBM API connect
    def ibm_api(self):
        response = requests.get("https://api.xforce.ibmcloud.com/xfti/mw/ipv4",
                                auth=HTTPBasicAuth('1f783594-dbd8-4884-9fd0-2c6fcc633415',
                                                   '83866f36-ffe7-4e5f-b931-e34307d83f82'))
        return json.dumps(response.json(), indent=4, sort_keys=True)
