#!/usr/bin/env python

import requests
import json

from CTIServerConnector.SuperConnector import SuperConnector


class INQUEST_LABS(SuperConnector):

    def __init__(self):
        super().__init__()


    # INQUEST LABS get CTIPs
    def api_con(self):
        response = requests.get("https://labs.inquest.net/api/iocdb/list")
        return json.dumps(response.json(), indent=4, sort_keys=True)
