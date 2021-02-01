#!/usr/bin/env python
from pymisp import PyMISP
from Utilities.utility import stix_to_json
from serviceDB.mongoDBService import ClientDB
from CTIServerConnector.SuperConnector import SuperConnector
import json


class MISP(SuperConnector):

    def __init__(self):
        super().__init__()

    # MISP get CTIPs
    def api_con(self):
        misp_url = 'https://127.0.0.1:8443'
        misp_key = 'p9Wz6OvifEEAwkoMZoLMsC9wgONd10E3q4wxLVQ5'
        misp_verifycert = False
        #run events,take uuids from each event with regex, run get_event(uuid) loop to take one by one
        misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)
        orgs = misp.organisations(scope="all")
        orgs_json = json.dumps(orgs, indent=4, sort_keys=True)
        orgs_parsed=json.loads(orgs_json)
        for x in range(len(orgs_parsed)):
            events=misp.search(controller="attributes",org=orgs_parsed[x]['Organisation']['name'])
            print((json.dumps(events, indent=4, sort_keys=True)))
            break


