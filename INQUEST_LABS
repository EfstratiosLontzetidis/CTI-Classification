#!/usr/bin/env python

import requests
import json
from CTIP import CTIP


class INQUEST_LABS(CTIP):
    pass

    def __init__(self):
        super().__init__()
        self.data = []


    # INQUEST LABS API connect
    def api_con(self):
        response = requests.get("https://labs.inquest.net/api/iocdb/list")
        return json.dumps(response.json(), indent=4, sort_keys=True)
