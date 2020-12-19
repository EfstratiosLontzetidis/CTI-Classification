#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth
from CTIServerConnector.SuperConnector import SuperConnector


class MRLOOQUER(SuperConnector):

    def __init__(self):
        super().__init__()

    # IBM get CTIPs
    def api_con(self):
        response = requests.get("https://iocfeed.mrlooquer.com/feed.json")
        return response.json()
