#!/usr/bin/env python
import requests, json
from CTIServerConnector.SuperConnector import SuperConnector
from stix2 import Report,Relationship,Identity,parse
from Utilities.utility import stix_to_json, convertCTIMEtoISOBLUELIV
from serviceDB.mongoDBService import ClientDB


class BLUELIV(SuperConnector):

    def __init__(self):
        super().__init__()

    def convert_ctips_to_stix2(self,response):
        x = json.loads(response.content.decode())
        ctips = json.dumps(x, indent=4)
        ctips_parsed = json.loads(ctips)
        for i in range(len(ctips_parsed)):
            if json.dumps(ctips_parsed[i]['id'], indent=4) not in spark_ids:
                spark_ids.append(json.dumps(ctips_parsed[i]['id']))
                if json.dumps(ctips_parsed[i]['user']['id'], indent=4) not in identity_ids:
                    # create identity
                    identity=Identity(name=ctips_parsed[i]['user']['username'])
                    print(identity)
                    print("----------------------------------------------------------------------------------")
                    iden=parse(identity)
                    Stix2Collection.insert_one(stix_to_json(iden))
                    identity_ids[str(json.dumps(ctips_parsed[i]['user']['id']))]=iden.id
                # create report
                report = Report(name=ctips_parsed[i]['title'],
                                description=ctips_parsed[i]['description'],
                                tags=ctips_parsed[i]['tags'],
                                created=convertCTIMEtoISOBLUELIV(ctips_parsed[i]['created_at']),
                                modified=convertCTIMEtoISOBLUELIV(ctips_parsed[i]['created_at']),
                                allow_custom=True,
                                tlp=ctips_parsed[i]['tlp'],
                                published=convertCTIMEtoISOBLUELIV(ctips_parsed[i]['created_at']),
                                object_refs=identity_ids[str(json.dumps(ctips_parsed[i]['user']['id']))],
                                report_type='threat-report')
                print(report)
                print("--------------------------------------------------------------------------------------")
                rep = parse(report,allow_custom=True)
                Stix2Collection.insert_one(stix_to_json(rep))
                # create relationship
                relationship = Relationship(relationship_type='references',
                                            source_ref=identity_ids[str(json.dumps(ctips_parsed[i]['user']['id']))],
                                            target_ref=rep.id)
                print(relationship)
                print("--------------------------------------------------------------------------------------")
                relat=parse(relationship)
                Stix2Collection.insert_one(stix_to_json(relat))



    def get_tags(self,response):
        #get all the tags from blueliv
        x = json.loads(response.content.decode())
        tags = json.dumps(x, indent=4)
        tags_parsed = json.loads(tags)
        name_tags=[]
        for i in range(len(tags_parsed)):
            name_tags.insert(i,json.dumps(tags_parsed[i]['name'], indent=4))
        return name_tags

    # Blueliv get CTIPs
    def api_con(self):
        # database
        global Stix2Collection
        Stix2Collection=ClientDB.db["CTIPsToStix2"]
        headers = {'Authorization':'Token c1ddf06a-5895-4ba0-a5bc-025f8caba1e9'}
        # get all tags
        tags = requests.get("https://community.blueliv.com/api/v1/tags/", headers=headers)
        name_tags=self.get_tags(tags)
        global identity_ids
        identity_ids={}
        global spark_ids
        spark_ids=[]
        # search for all tags
        for x in range(len(name_tags)):
            response = requests.get("https://community.blueliv.com/api/v1/tags/"+name_tags[x].strip('"')+"/sparks", headers=headers)
            self.convert_ctips_to_stix2(response)




