import requests, json
from CTIServerConnector.SuperConnector import SuperConnector


class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()

    # Blueliv get CTIPs
    def api_con(self):
        headers = {'Authorization':'Token c1ddf06a-5895-4ba0-a5bc-025f8caba1e9'}
        response = requests.get("https://community.blueliv.com/api/v1/tags/MALWARE/sparks", headers=headers)
        x=json.loads(response.content.decode())
        return json.dumps(x, indent=4)
