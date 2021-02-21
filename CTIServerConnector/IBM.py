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
        response = requests.get("https://api.xforce.ibmcloud.com/xfti/c2server/ipv4",
                                auth=HTTPBasicAuth('2318b0d2-8183-46fc-8026-7dda8c11aa99',
                                                   '2baec270-50e3-4592-aae7-cfa2a2df0574'),verify=False)
        return response
