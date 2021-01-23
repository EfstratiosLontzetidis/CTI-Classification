#!/usr/bin/env python

import requests, json
from stix2 import Malware, Indicator, Relationship, parse
from requests.auth import HTTPBasicAuth
from Utilities.utility import convertCtimeToISOFormatOTXmalwares, convertCtimeToISOFormatOTXiocs, stix_to_json
from serviceDB.mongoDBService import ClientDB
from CTIServerConnector.SuperConnector import SuperConnector


class OTX(SuperConnector):

    def __init__(self):
        super().__init__()

    def indicators_malwares_relationships_stix2(self,CTIP):
        #db name
        Stix2Collection = ClientDB.db["CTIPsToStix2"]
        CTIP_json = json.dumps(CTIP.json(), indent=4, sort_keys=True)
        # parsing the json CTIPs
        CTIP_json_parsed = json.loads(CTIP_json)
        for x in range(len(CTIP_json_parsed['results'])):
            if len(CTIP_json_parsed['results'][x]['malware_families'])==0:
                is_family=False
                aliases=""
            else:
                is_family=True
                aliases=CTIP_json_parsed['results'][x]['malware_families']
            malware=Malware(name=CTIP_json_parsed['results'][x]['name'],
                            allow_custom=True,
                            created_by=CTIP_json_parsed['results'][x]['author_name'],
                            tlp=CTIP_json_parsed['results'][x]['TLP'],
                            description=CTIP_json_parsed['results'][x]['description'],
                            aliases=aliases,
                            created=convertCtimeToISOFormatOTXmalwares(CTIP_json_parsed['results'][x]['created']),
                            modified=convertCtimeToISOFormatOTXmalwares(CTIP_json_parsed['results'][x]['modified']),
                            tags=CTIP_json_parsed['results'][x]['tags'],
                            targeted_countries=CTIP_json_parsed['results'][x]['targeted_countries'],
                            adversary=CTIP_json_parsed['results'][x]['adversary'],
                            is_family=is_family)
            print(malware)
            STIX_malware_parsed=parse(malware, allow_custom=True)
            #store malware in db
            Stix2Collection.insert_one(stix_to_json(STIX_malware_parsed))
            malware_id=STIX_malware_parsed.id
            #for each malware, bring me its indicators
            for y in range(len(CTIP_json_parsed['results'][x]['indicators'])):
                try:
                    #check if indicator has a name,otherwise i give him a custom name
                    if CTIP_json_parsed['results'][x]['indicators'][y]['title']=="":
                        name="Indicator-name-"+str(CTIP_json_parsed['results'][x]['indicators'][y]['id'])
                    else:
                        name=CTIP_json_parsed['results'][x]['indicators'][y]['title']
                    #check indicator types
                    if CTIP_json_parsed['results'][x]['indicators'][y]['type']=="domain":
                        pattern="[domain-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="IPv4":
                        pattern="[ipv4-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="IPv6":
                        pattern="[ipv6-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="URL":
                        pattern="[url-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="hostname":
                        pattern="[hostname-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="email":
                        pattern="[email-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="URI":
                        pattern="[uri-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FileHash-MD5":
                        pattern="[md5-hash:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FileHash-SHA1":
                        pattern="[sha1-hash:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FileHash-SHA256":
                        pattern="[sha256-hash:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FileHash-PEHASH":
                        pattern="[pe-hash:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FileHash-IMPHASH":
                        pattern="[imp-hash:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="CIDR":
                        pattern="[cidr-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="FilePath":
                        pattern="[file-path:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="Mutex":
                        pattern="[mutex-rsc:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="CVE":
                        pattern="[cve-entry:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="YARA":
                        pattern="[yara-rule:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="JA3":
                        pattern="[ja3-sign:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="osquery":
                        pattern="[osq-rule:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    elif CTIP_json_parsed['results'][x]['indicators'][y]['type']=="SSLCertFingerprint":
                        pattern="[ssl-fing:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    else:
                        pattern ="[bitcoin-addr:value = "+"'"+CTIP_json_parsed['results'][x]['indicators'][y]['indicator']+"'"+"]"
                    #check if the indicator is active
                    if CTIP_json_parsed['results'][x]['indicators'][y]['indicator']==1:
                        is_active=True
                    else:
                        is_active=False
                    #check for valid date formats
                    if CTIP_json_parsed['results'][x]['indicators'][y]['expiration']==None:
                        valid_until="2022-01-23T10:43:21Z"
                    else:
                        valid_until=convertCtimeToISOFormatOTXiocs(CTIP_json_parsed['results'][x]['indicators'][y]['expiration'])

                    indicator=Indicator(name=name,
                                        created=convertCtimeToISOFormatOTXiocs(CTIP_json_parsed['results'][x]['indicators'][y]['created']),
                                        valid_until=valid_until,
                                        description=CTIP_json_parsed['results'][x]['indicators'][y]['description'],
                                        indicator=CTIP_json_parsed['results'][x]['indicators'][y]['indicator'],
                                        allow_custom=True,
                                        pattern_type="stix",
                                        pattern=pattern,
                                        is_active=is_active,
                                        indicator_types="malicious-activity")
                    print(indicator)
                    #parse the stix ioc and take its id in order to make a relationship and store him in db
                    STIX_ioc_parsed = parse(indicator, allow_custom=True)
                    Stix2Collection.insert_one(stix_to_json(STIX_ioc_parsed))
                    ioc_id = STIX_ioc_parsed.id
                    #create the relationship
                    relationship=Relationship(relationship_type='indicates',
                                              source_ref=ioc_id,
                                              target_ref=malware_id)
                    print(relationship)
                    STIX_relationship_parsed=parse(relationship,allow_custom=True)
                    Stix2Collection.insert_one(stix_to_json(STIX_relationship_parsed))
                except Exception:
                    continue

        return CTIP_json_parsed['next']




    # OTX get CTIPs
    def api_con(self):
        # can take pulses using id,so can be taken one by one using regex

        response = requests.get("https://otx.alienvault.com/api/v1/pulses/activity",
                                auth=HTTPBasicAuth('34c7431b6d78523543910d7bdc04e2126849a8b583814c263ae9ef84b9ec58ca',
                                                   ''))
        next=self.indicators_malwares_relationships_stix2(response)
        while(next is not None):
            response=requests.get(next,
                                auth=HTTPBasicAuth('34c7431b6d78523543910d7bdc04e2126849a8b583814c263ae9ef84b9ec58ca',
                                                   ''))
            try:
                next=self.indicators_malwares_relationships_stix2(response)
            except Exception:
                break
