#!/usr/bin/env python

import requests
import json
from stix2 import Malware, Infrastructure, parse
from serviceDB.mongoDBService import ClientDB
from Utilities.utility import convertCtimeToISOFormatURLHAUS, stix_to_json

from CTIServerConnector.SuperConnector import SuperConnector


class URLHAUS(SuperConnector):

    def __init__(self):
        super().__init__()


    def payloads_json(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        Stix2Collection = ClientDB.db["URLHAUS_JSON"]
        for x in range(len(parsed_CTIPs['payloads'])):
            Stix2Collection.insert_one(parsed_CTIPs['payloads'][x])


    def urls_json(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/urls/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        Stix2Collection = ClientDB.db["URLHAUS_JSON"]
        for x in range(len(parsed_CTIPs['urls'])):
            Stix2Collection.insert_one(parsed_CTIPs['urls'][x])


    def payloads_to_stix2_malwares(self):
        response = requests.get("https://urlhaus-api.abuse.ch/v1/payloads/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        malware_ids={}
        for x in range(len(parsed_CTIPs['payloads'])):
            #check if the object represents a malware family
            if parsed_CTIPs['payloads'][x]['signature'] is None:
                is_family=False
                aliases=""
            else:
                is_family=True
                aliases=parsed_CTIPs['payloads'][x]['signature']

            malware=Malware(name="Malware payload",
                            is_family=is_family,
                            aliases=aliases,
                            allow_custom=True,
                            created=convertCtimeToISOFormatURLHAUS(parsed_CTIPs['payloads'][x]['firstseen']),
                            md5_hash=parsed_CTIPs['payloads'][x]['md5_hash'],
                            sha256_hash=parsed_CTIPs['payloads'][x]['sha256_hash'],
                            file_type=parsed_CTIPs['payloads'][x]['file_type'],
                            first_seen=convertCtimeToISOFormatURLHAUS(parsed_CTIPs['payloads'][x]['firstseen']),
                            imphash=parsed_CTIPs['payloads'][x]['imphash'],
                            ssdeephash=parsed_CTIPs['payloads'][x]['ssdeep'],
                            tlshash=parsed_CTIPs['payloads'][x]['tlsh'],
                            file_size=parsed_CTIPs['payloads'][x]['file_size'])
            print(malware)
            # parse the stix2 object
            stix2_malware_parsed = parse(malware, allow_custom=True)
            # store it in db
            Stix2Collection = ClientDB.db["URLHAUS_STIX2"]
            Stix2Collection.insert_one(stix_to_json(stix2_malware_parsed))

    def urls_to_stix2_infrastructures(self):
        response=requests.get("https://urlhaus-api.abuse.ch/v1/urls/recent/")
        CTIPs = json.dumps(response.json(), indent=4, sort_keys=True)
        parsed_CTIPs = json.loads(CTIPs)
        for x in range(len(parsed_CTIPs['urls'])):
            infrastructure=Infrastructure(name="URL: "+parsed_CTIPs['urls'][x]['url']+ " hosting malicious payloads",
                                          infrastructure_types="hosting-malware",
                                          allow_custom=True,
                                          url=parsed_CTIPs['urls'][x]['url'],
                                          created=convertCtimeToISOFormatURLHAUS(parsed_CTIPs['urls'][x]['date_added']),
                                          url_status=parsed_CTIPs['urls'][x]['url_status'],
                                          host=parsed_CTIPs['urls'][x]['host'],
                                          blacklists=parsed_CTIPs['urls'][x]['blacklists'],
                                          created_by=parsed_CTIPs['urls'][x]['reporter'],
                                          tags=parsed_CTIPs['urls'][x]['tags'])
            print(infrastructure)
            # parse the stix2 object
            stix2_infrastructure_parsed = parse(infrastructure, allow_custom=True)
            #store it in db
            Stix2Collection = ClientDB.db["URLHAUS_STIX2"]
            Stix2Collection.insert_one(stix_to_json(stix2_infrastructure_parsed))

    # URLhaus get CTIPs
    def api_con(self):
        self.payloads_json()
        self.urls_json()
        self.payloads_to_stix2_malwares()
        self.urls_to_stix2_infrastructures()

