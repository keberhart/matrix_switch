#!/usr/bin/env python

#
#   A driver class for the telnet controlled matrix switches
#
import telnetlib
import logging

class MatSwitch(object):
    def __init__(self, address, port=None):
        self.logger = logging.getLogger(__name__)
        self.address = address
        self.port = port
        self.target = None
        self.status = {}

    def __repr__(self):
        return "<MatSwitch('%s', '%s')>" % (self.address, self.port)

    def connect(self):
        try:
            self.target = telnetlib.Telnet(self.address,self.port)
        except:
            self.error = True
            self.errorMsg = "Failed to connect to device: %s" % self.__repr__()
            self.logger.debug(self.errorMsg)
            raise RuntimeError(self.errorMsg)

    def getStatus(self):
        if self.target is None:
            self.connect()
        try:
            self.target.write('5\r')
            self.status = self.target.read_eager()
            return self.status
        except:
            self.error = True
            self.errorMsg = "getDevice failed on device: %s" % self.__repr__()
            self.logger.debug(self.errorMsg)
            raise RuntimeError(self.errorMsg)

    def setDevice(self, position):
        if self.target is None:
            self.connect()
        try:
            self.target.write(position+'\r')
            self.getStatus()
        except:
            self.error = True
            self.errorMsg = "setDevice failed on device: %s" % self.__repr__()
            self.logger.debug(self.errorMsg)
            raise RuntimeError(self.errorMsg)

    def close(self):
        self.target.close()
        self.target = None

