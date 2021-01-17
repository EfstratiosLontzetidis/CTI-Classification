#!/usr/bin/env python

import requests, json, re
from stix2 import Malware, Indicator, Relationship, parse
from Utilities.utility import datetimeconvertforpulsedive, portspulsedive, manyvaluespulsedive, stix_to_json
from serviceDB.mongoDBService import ClientDB
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
        # check if hosttype exist
        try:
            # take hosttype of malware's activity
            hosttype = manyvaluespulsedive((response_json_parsed['summary']['attributes']['hosttype']))
        except Exception:
            hosttype = ""
        # check if technologies exist
        try:
            # take technologies of malware's activity
            technologies = manyvaluespulsedive(response_json_parsed['summary']['attributes']['technology'])
        except Exception:
            technologies = ""
        # check if protocols exist
        try:
            # take protocols of malware's activity
            protocols = manyvaluespulsedive(response_json_parsed['summary']['attributes']['protocol'])
        except Exception:
            protocols = ""
        # check if ports exist
        try:
            # take ports of malware's activity
            ports = portspulsedive(response_json_parsed['summary']['attributes']['port'])
        except Exception:
            ports = ""
        # check if othernames exist
        try:
            othernames=response_json_parsed['othernames']
        except Exception:
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
                          hosttype=hosttype,
                          protocols=protocols,
                          allow_custom=True,
                          is_family=False)
        return malware

    def indicators_to_stix2(self, ctip, threats_list):
        # parse json
        global threats
        response_json_parsed = json.loads(ctip)
        # convert datetimes of seen,added,updated to datetime objects in stix2 standard
        stamp_seen_datetime = datetimeconvertforpulsedive(response_json_parsed['stamp_seen'])
        stamp_added_datetime = datetimeconvertforpulsedive(response_json_parsed['stamp_added'])
        stamp_updated_datetime = datetimeconvertforpulsedive(response_json_parsed['stamp_updated'])
        #include the risk
        risk=response_json_parsed['risk']
        # check if hosttype exist
        try:
            # take hosttype of indicator's activity
            hosttype = manyvaluespulsedive((response_json_parsed['attributes']['hosttype']))
        except Exception:
            hosttype = ""
        # check if technologies exist
        try:
            # take technologies of indicator's activity
            technologies = manyvaluespulsedive(response_json_parsed['attributes']['technology'])
        except Exception:
            technologies = ""
        # check if protocols exist
        try:
            # take protocols of indicator's activity
            protocols = manyvaluespulsedive(response_json_parsed['attributes']['protocol'])
        except Exception:
            protocols = ""
        # check if ports exist
        try:
            # take ports of indicator's activity
            ports = portspulsedive(response_json_parsed['attributes']['port'])
        except Exception:
            ports = ""

        properties=str(response_json_parsed['properties']).replace('.',"")
        indicator="'"+response_json_parsed['indicator']+"'"

        if response_json_parsed['type']=="ip":
            name="Malware Ip"
            domain=""
            pattern="[ipv4-addr:value = "+indicator+"]"
        else :
            name="Malware domain"
            try:
                domain=response_json_parsed['domain']
            except Exception:
                domain=indicator
            pattern="[domain-addr:value = "+indicator+"]"


        #create indicator object
        indicator=Indicator(name=name,
                            pattern=pattern,
                            pattern_type="stix",
                            first_seen=stamp_seen_datetime,
                            created=stamp_added_datetime,
                            modified=stamp_updated_datetime,
                            risk=response_json_parsed['risk'],
                            technologies=technologies,
                            ports=ports,
                            hosttype=hosttype,
                            protocols=protocols,
                            properties=properties,
                            allow_custom=True)

        print("=================================================")
        print(indicator)

        # parse the stix2 object
        CTIP_ioc_parsed = parse(indicator, allow_custom=True)
        #store it in database
        Stix2Collection = ClientDB.db["CTIPsToStix2"]
        Stix2Collection.insert_one(stix_to_json(CTIP_ioc_parsed))
        #ioc id for relationship objects
        ioc_id=CTIP_ioc_parsed.id
        # for relationships stix2 objects
        #check if indicator has threats
        try:
            threats=json.dumps(response_json_parsed['threats'])
            has="threats"
        except Exception:
            has = "no threats"
        if has=="threats":
            linked_malwares = re.findall('(?:tid": )(\d+)', str(threats))
            for x in range(len(linked_malwares)):
                if int(linked_malwares[x]) in threats_list:
                    malware_id=threats_list[int(linked_malwares[x])]
                    relationship=Relationship(relationship_type='indicates',
                                                  source_ref=ioc_id,
                                                  target_ref=malware_id)
                    print("=========================================================")
                    print(relationship)
                    # parse the stix2 object
                    CTIP_relationship_parsed=parse(relationship)
                    # store it in database
                    Stix2Collection.insert_one(stix_to_json(CTIP_relationship_parsed))

    # PULSEDIVE get CTIPs
    def api_con(self):
        #need to automate malwares
        threat_id_malware_id = {}
        for x in range(300):
            response = requests.get("https://pulsedive.com/api/info.php?tid="+str(x)+"&pretty=1&key=ccb008a66b43702e60bf2606826272f1a18730d718070383bb4beb17b7b6c31b")
            if response.status_code==200:
                response_json=json.dumps(response.json(), indent=4, sort_keys=True)
                malware_stix2=self.threats_to_stix2(response_json)
                print(malware_stix2)
                #parse the stix2 object
                CTIP_parsed=parse(malware_stix2, allow_custom=True)
                #store threat id from pulsedive and malware object id for later in order to make relationships with indicators
                threat_id_malware_id[x]=CTIP_parsed.id
                #store it in database
                Stix2Collection = ClientDB.db["CTIPsToStix2"]
                Stix2Collection.insert_one(stix_to_json(CTIP_parsed))

        # #indicators by id, if they have threats linked, will be combined to stix2 relationship
        for y in range(300):
            response2=requests.get("https://pulsedive.com/api/info.php?iid="+str(y)+"&historical=0&schema=1&pretty=1&key=ccb008a66b43702e60bf2606826272f1a18730d718070383bb4beb17b7b6c31b")
            if response2.status_code==200:
                response2_json = json.dumps(response2.json(), indent=4, sort_keys=True)
                self.indicators_to_stix2(response2_json, threat_id_malware_id)
