#!/usr/bin/env python
from abc import abstractmethod, ABC


class SuperConnector(object):

    def __init__(self):
        pass

    @abstractmethod
    def api_con(self):
        return

    def setConnectorBehaviour(self, conn_obj):
        self.conn_beh_obj = conn_obj

    def getCTIPs(self):
        ctips = self.conn_beh_obj.api_con()
        return ctips

