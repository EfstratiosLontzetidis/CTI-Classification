from CTIServerConnector.MISP import MISP
from CTIServerConnector.OTX import OTX
from CTIServerConnector.SuperConnector import SuperConnector
from CTIServerConnector.IBM import IBM
from CTIServerConnector.URLHAUS import URLHAUS
from CTIServerConnector.OPENCTI import OPENCTI
from stix2validator import validate_file, print_results

connector = SuperConnector()
connection_behavior = OPENCTI()
connector.setConnectorBehaviour(connection_behavior)

ctips = connector.getCTIPs()
print(ctips)

#results = validate_file("ctifeed2.json")
#print_results(results)
