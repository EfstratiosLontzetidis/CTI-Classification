#!/usr/bin/env python

import requests
import json

from CTIServerConnector.SuperConnector import SuperConnector


class MISP(SuperConnector):

    def __init__(self):
        super().__init__()


    # MISP get CTIPs
    def api_con(self):
        url = 'https://www.circl.lu/doc/misp/feed-osint/'
        response = requests.get('{}manifest.json'.format(url))
        return (json.dumps(response.json(), indent=4, sort_keys=True))
