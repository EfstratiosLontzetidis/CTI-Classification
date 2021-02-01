#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
from CTIServerConnector.SuperConnector import SuperConnector

#needs api id and key refresh
class IBM(SuperConnector):

    def __init__(self):
        super().__init__()

    # IBM get CTIPs
    def api_con(self):
        #IBM will may be dropped,cause of free trial
        response = requests.get("https://api.xforce.ibmcloud.com/auth/api_key",
                                auth=HTTPBasicAuth('b8ff51dd-89d2-40f2-a289-3e0768361ea0',
                                                   '17d90598-768e-4b6c-b03b-1d70c4475aca'),verify=False)
        return response
