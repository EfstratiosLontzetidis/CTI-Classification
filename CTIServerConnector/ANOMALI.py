from taxii2client.v20 import Server, Collection
from CTIServerConnector.SuperConnector import SuperConnector

class ANOMALI(SuperConnector):

    def __init__(self):
        super().__init__()

    # OpenCTI get CTIPs
    def api_con(self):

        server = Server("https://cti-taxii.mitre.org/taxii/")

        api_root = server.api_roots[0]

        server = Server("https://limo.anomali.com/api/v1/taxii2/feeds/", user="guest", password="guest")

        collection = api_root.collections[0]
        return collection.get_objects()

