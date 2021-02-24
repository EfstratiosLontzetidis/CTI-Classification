#!/usr/bin/env python
from Utilities.utility import stix_to_json
from serviceDB.mongoDBService import ClientDB
from CTIServerConnector.SuperConnector import SuperConnector
from stix2 import parse
import json


class MISP(SuperConnector):

    def __init__(self):
        super().__init__()

    # MISP get CTIPs
    def api_con(self):

        Stix2Collection = ClientDB.db["CTIPsToStix2"]
        # misp instance credentials
        misp_url = 'http://127.0.0.1:80'
        misp_key = 'KAmW8Eur8wkbepUvMA8BMiwkij27uioujgQkATVc'
        misp_verifycert = False
        # connect to MISP instance
        # misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)
        # generated and downloaded the events in stix2 from MISP GUI and place them in a file
        # then pulled every stix2 CTIP and place it in database
        with open("misp.stix2.ADMIN.json", "r") as file:
            jsonfile=json.load(file)
            for x in range(len(jsonfile['objects'])):
                ctip=json.dumps(jsonfile['objects'][x], indent=4)
                print(ctip)
                print("-----------------------------------------------------")
                try:
                    CTIP_parsed = parse(ctip, allow_custom=True)
                    Stix2Collection.insert_one(stix_to_json(CTIP_parsed))
                except Exception:
                    continue

