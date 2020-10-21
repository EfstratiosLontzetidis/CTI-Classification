from CTIServerConnector.SuperConnector import SuperConnector
from CTIServerConnector.IBM import IBM



connector = SuperConnector()
connection_behavior = IBM()
connector.setConnectorBehaviour(connection_behavior)

ctips = connector.getCTIPs()
print(ctips)

