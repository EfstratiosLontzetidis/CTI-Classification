import requests
from CTIServerConnector.SuperConnector import SuperConnector


class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()

    # IBM get CTIPs
    def api_con(self):
        headers = {'Authorization':'Token 30ab82b2-dd75-4dc5-9f34-4209fa3e933c'}
        response = requests.get("https://community.blueliv.com/api/v1/users/omarbv/sparks",headers=headers)
        return  response.json()
