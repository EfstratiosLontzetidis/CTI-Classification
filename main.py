from stix2 import FileSystemStore
from stix2 import parse

from CTIServerConnector.ANOMALI import ANOMALI
from CTIServerConnector.BLUELIV import BLUELIV
from CTIServerConnector.MRLOOQUER import MRLOOQUER
from CTIServerConnector.OPENCTI import OPENCTI
from CTIServerConnector.MISP import MISP
from CTIServerConnector.OTX import OTX
from CTIServerConnector.PULSEDIVE import PULSEDIVE
from CTIServerConnector.SuperConnector import SuperConnector
from CTIServerConnector.IBM import IBM
from CTIServerConnector.URLHAUS import URLHAUS

connector = SuperConnector()
connection_behavior = URLHAUS()
connector.setConnectorBehaviour(connection_behavior)

ctips = connector.getCTIPs()
#print(ctips)
#from Utilities.utility import stix_to_json
#from serviceDB.mongoDBService import ClientDB

#maliciousEmailAttachmentsCollection = ClientDB.db['emailAttachment']


#file_handle = open("./samples/bundle--0ad822db-6962-44a4-bc14-5f178a1dbb3f.json")

#anEmailSample = parse(file_handle, allow_custom=True)

#maliciousEmailAttachmentsCollection.insert_one(stix_to_json(anEmailSample))