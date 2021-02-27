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

