#!/usr/bin/env python
from pymisp import PyMISP
from CTIServerConnector.SuperConnector import SuperConnector


class MISP(SuperConnector):

    def __init__(self):
        super().__init__()

    # MISP get CTIPs
    def api_con(self):
        misp_url = 'https://127.0.0.1:8443'
        misp_key = 'p9Wz6OvifEEAwkoMZoLMsC9wgONd10E3q4wxLVQ5'
        misp_verifycert = False

        misp = PyMISP(misp_url, misp_key, misp_verifycert, debug=False)
        data = misp.events()
        return (data)
