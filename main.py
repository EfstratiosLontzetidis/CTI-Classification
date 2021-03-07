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
from CTIServerConnector.MITRE import MITRE

# connector = SuperConnector()
# connection_behavior = OPENCTI()
# connector.setConnectorBehaviour(connection_behavior)
#
# ctips = connector.getCTIPs()
# print(ctips)
import stix2
from stix2 import FileSystemStore

fs = FileSystemStore("./filesystemlocalrepository")

# retrieve STIX2 content from FileSystemStore
mal = fs.get("malware--92ec0cbd-2c30-44a2-b270-73f4ec949841")

# for visual purposes
print(mal)

