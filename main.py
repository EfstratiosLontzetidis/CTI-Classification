from CTIServerConnector.SuperConnector import SuperConnector
from CTIServerConnector.MISP import MISP
from CTIServerConnector.OTX import OTX
from CTIServerConnector.IBM import IBM
from CTIServerConnector.URLHAUS import URLHAUS



connector = SuperConnector()
connection_behavior = MISP()
connector.setConnectorBehaviour(connection_behavior)

ctips = connector.getCTIPs()
print(ctips)

