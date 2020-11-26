import requests
import json
import logging
from requests.auth import HTTPBasicAuth
from CTIServerConnector.SuperConnector import SuperConnector
from sdk.blueliv_api import BluelivAPI


#!!!!not ready to run,needs config to its token!!!!

class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()
        

    # IBM get CTIPs
    def api_con(self):
        #headers = {'Authorization':'c64a84cd-e759-49c4-b66a-b5c2d0487b27'}
        #response = requests.get("https://community.blueliv.com/api/v1/iocs/types",headers=headers)
        #return json.dumps(response.json(), indent=4, sort_keys=True)
        #return  response.status_code

        api = BluelivAPI(base_url='https://api.blueliv.com',token='c64a84cd-e759-49c4-b66a-b5c2d0487b27')
        response=api.malwares.last()
        return response
