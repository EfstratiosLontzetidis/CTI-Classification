#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth

from CTIServerConnector.SuperConnector import SuperConnector


class OTX(SuperConnector):

    def __init__(self):
        super().__init__()
    
    # OTX get CTIPs
    def api_con(self):
        #can take pulses using id,so can be taken one by one using regex
        response = requests.get("https://otx.alienvault.com/api/v1/pulses/5fe4cb300b0a9b6655a11de1/",
                                auth=HTTPBasicAuth('34c7431b6d78523543910d7bdc04e2126849a8b583814c263ae9ef84b9ec58ca',
                                                   ''))
        return json.dumps(response.json(), indent=4, sort_keys=True)
