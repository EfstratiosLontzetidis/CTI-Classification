#!/usr/bin/env python

import requests
import json
from stix2 import parse, Indicator
from Utilities.utility import stix_to_json, convertCtimeToISOFormatMRLooquer
from serviceDB.mongoDBService import ClientDB
from CTIServerConnector.SuperConnector import SuperConnector


class MRLOOQUER(SuperConnector):

    def __init__(self):
        super().__init__()

    # MRLOOQUER get CTIPs,csv ,not one by one
    def api_con(self):
        response = requests.get("https://iocfeed.mrlooquer.com/feed.json")
        #parse the converted json
        parsed_CTIP=json.loads(json.dumps(response.json(), indent=4))
        for x in range(len(parsed_CTIP)):
            # check indicator type
            if parsed_CTIP[x]['category']=="malware":
                type_ov="malicious-activity"
            elif parsed_CTIP[x]['category']=="fraud":
                type_ov="anomalous-activity"
            else:
                type_ov="anonymization"

            pattern="[ipv4-addr:value = "+"'"+parsed_CTIP[x]['ip4']+"'"+" AND ipv6-addr:value = "+"'"+parsed_CTIP[x]['ip6']+"'" +"]"
            try:
                indicator=Indicator(name="Indicators - Dual stack (IPv4 and IPv6 for domain: "+parsed_CTIP[x]['domain']+")",
                                    pattern=pattern,
                                    pattern_type="stix",
                                    indicator_types=type_ov,
                                    subcategory=parsed_CTIP[x]['subcategory'],
                                    categorytype=parsed_CTIP[x]['type'],
                                    domain=parsed_CTIP[x]['domain'],
                                    created=convertCtimeToISOFormatMRLooquer(parsed_CTIP[x]['lastSeen']),
                                    modified=convertCtimeToISOFormatMRLooquer(parsed_CTIP[x]['lastSeen']),
                                    last_seen=convertCtimeToISOFormatMRLooquer(parsed_CTIP[x]['lastSeen']),
                                    allow_custom=True,
                                    iPv4=parsed_CTIP[x]['ip4'],
                                    iPv4ASN=parsed_CTIP[x]['ip4Asn'],
                                    iPv4NumberOfCVE=parsed_CTIP[x]['ip4NumCve'],
                                    iPv4Ports=parsed_CTIP[x]['ip4Portlist'],
                                    iPv6=parsed_CTIP[x]['ip6'],
                                    iPv6Prefix=parsed_CTIP[x]['ip6Prefix'],
                                    iPv6ASN=parsed_CTIP[x]['ip6Asn'],
                                    iPv6NumberOfCVE=parsed_CTIP[x]['ip6NumCve'],
                                    iPv6Ports=parsed_CTIP[x]['ip6Portlist'],
                                    valid_from=convertCtimeToISOFormatMRLooquer(parsed_CTIP[x]['lastSeen'])
                                    )
                # parse the stix2 object
                CTIP_ioc_parsed = parse(indicator, allow_custom=True)
                # store it in database
                Stix2Collection = ClientDB.db["CTIPsToStix2"]
                Stix2Collection.insert_one(stix_to_json(CTIP_ioc_parsed))
                print(indicator)
            except KeyError:
                continue

