import requests
import json
from requests.auth import HTTPBasicAuth


class OTX:

    def __init__(self):
        self.data = []

    
    # OTX API connect
    def otx_api(self):
        response = requests.get("https://otx.alienvault.com/api/v1/pulses/activity",
                                auth=HTTPBasicAuth('34c7431b6d78523543910d7bdc04e2126849a8b583814c263ae9ef84b9ec58ca',
                                                   ''))
        return json.dumps(response.json(), indent=4, sort_keys=True)
