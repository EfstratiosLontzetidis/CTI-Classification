#!/usr/bin/env python
from Utilities.utility import stix_to_json, convertCTIMEtoISOBLUELIV
from serviceDB.mongoDBService import ClientDB
from taxii2client.v20 import Server
from CTIServerConnector.SuperConnector import SuperConnector
import json
from stix2 import parse

class MITRE(SuperConnector):

    def __init__(self):
        super().__init__()

    # MITRE get CTIPs
    def api_con(self):
        Stix2Collection = ClientDB.db["MITRE_STIX2"]
        server=Server("https://cti-taxii.mitre.org/taxii/")
        api_root=server.api_roots[0]
        for x in range(len(api_root.collections)):
            print("Starting collection number: " + str(x))
            collection = api_root.collections[x]
            collection_json= json.dumps(collection.get_objects(), indent=4)
            ctips_parsed = json.loads(collection_json)
            for y in range(len(ctips_parsed['objects'])):
                CTIP = parse(ctips_parsed['objects'][y], allow_custom=True)
                try:
                    Stix2Collection.insert_one(stix_to_json(CTIP))
                    print(CTIP)
                except AttributeError:
                    continue
