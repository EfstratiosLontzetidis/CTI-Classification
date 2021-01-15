#!/usr/bin/env python

import requests, json
from stix2 import Malware
from Utilities.utility import datetimeconvertforpulsedive, portspulsedive, protocolspulsedive, technologiespulsedive
from CTIServerConnector.SuperConnector import SuperConnector


class PULSEDIVE(SuperConnector):

    def __init__(self):
        super().__init__()

    def threats_to_stix2(self, ctip):
        #parse json
        response_json_parsed = json.loads(ctip)
        # convert datetimes of seen,added,updated to datetime objects in stix2 standard
        stamp_seen_datetime=datetimeconvertforpulsedive(response_json_parsed['stamp_seen'])
        stamp_added_datetime = datetimeconvertforpulsedive(response_json_parsed['stamp_added'])
        stamp_updated_datetime=datetimeconvertforpulsedive(response_json_parsed['stamp_updated'])
        # check if technologies exist
        try:
            # take technologies of malware's activity
            technologies = technologiespulsedive(response_json_parsed['summary']['attributes']['technology'])
        except TypeError:
            technologies = ""
        # check if protocols exist
        try:
            # take protocols of malware's activity
            protocols = protocolspulsedive(response_json_parsed['summary']['attributes']['protocol'])
        except TypeError:
            protocols = ""
        # check if ports exist
        try:
            # take ports of malware's activity
            ports = portspulsedive(response_json_parsed['summary']['attributes']['port'])
        except TypeError:
            ports = ""
        # check if othernames exist
        try:
            othernames=response_json_parsed['othernames']
        except KeyError:
            othernames=""
        # make the malware object
        malware = Malware(name=response_json_parsed['threat'],
                          description=response_json_parsed['wikisummary'],
                          first_seen=stamp_seen_datetime,
                          created=stamp_added_datetime,
                          modified=stamp_updated_datetime,
                          risk=response_json_parsed['risk'],
                          aliases=othernames,
                          technologies=technologies,
                          ports=ports,
                          protocols=protocols,
                          allow_custom=True,
                          is_family=False)
        return malware

    #not done yet
    def indicators_to_stix2(self, ctip):
        return

    # PULSEDIVE get CTIPs
    def api_con(self):
        #threats by id,can make a loop to take each one, problem when threat not found (tid=2 for example)**
        response = requests.get("https://pulsedive.com/api/info.php?tid=11&pretty=1&key=ccb008a66b43702e60bf2606826272f1a18730d718070383bb4beb17b7b6c31b")
        response_json=json.dumps(response.json(), indent=4, sort_keys=True)
        malware_stix2=self.threats_to_stix2(response_json)
        return malware_stix2


        #indicators by id, if they have threats, will be combined to stix2 relationship



        #write CTIP in file for analysis
        # file='15.json'
        # with open(file, 'w') as outfile:
        #     outfile.write(json.dumps(response.json(), indent=4, sort_keys=True))
        # return json.dumps(response.json(), indent=4, sort_keys=True)
