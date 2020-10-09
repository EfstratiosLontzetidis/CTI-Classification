#!/usr/bin/env python

import requests
import json
from requests.auth import HTTPBasicAuth


#IBM API connect
def ibm_api():
    response = requests.get("https://api.xforce.ibmcloud.com/xfti/mw/ipv4", auth = HTTPBasicAuth('1f783594-dbd8-4884-9fd0-2c6fcc633415','83866f36-ffe7-4e5f-b931-e34307d83f82'))
    return json.dumps(response.json(), indent=4, sort_keys=True)

#OTX API connect
def otx_api():
    response = requests.get("https://otx.alienvault.com/api/v1/pulses/activity", auth = HTTPBasicAuth('34c7431b6d78523543910d7bdc04e2126849a8b583814c263ae9ef84b9ec58ca',''))
    return json.dumps(response.json(), indent=4, sort_keys=True)


pulses=otx_api()
print(pulses)
