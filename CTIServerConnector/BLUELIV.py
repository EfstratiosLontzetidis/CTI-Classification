import requests, json
from CTIServerConnector.SuperConnector import SuperConnector


class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()

    # IBM get CTIPs
    def api_con(self):
        #can't seperate the feeds, thus can't transform in json
        headers = {'Authorization':'Token 35de5f77-8dec-48eb-89f2-92c7b1ee37e2'}
        #by tags
        #response = requests.get("https://community.blueliv.com/api/v1/tags", headers=headers)
        response = requests.get("https://community.blueliv.com/api/v1/tags/MALWARE/sparks", headers=headers)
        #by id of spark is not showing everything
        # response = requests.get("https://community.blueliv.com/api/v1/sparks/5f8f0b8482df413eaf3440ec", headers=headers)
        #by blueliv
        #response = requests.get("https://community.blueliv.com/api/v1/users/Blueliv/sparks",headers=headers)
        return response.content
