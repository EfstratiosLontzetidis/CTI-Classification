
from CTIFeedConnector import CTIFeedConnector

con = CTIFeedConnector()

pulses = con.urlhaus_api()
print(pulses)