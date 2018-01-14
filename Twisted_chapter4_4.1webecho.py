from twisted.protocols import basic
from twisted.internet import protocol, reactor
from twisted.logger import globalLogBeginner, textFileLogObserver
import sys


class HTTPEchoProtocol(basic.LineReceiver):
    def __init__(self):
        self.lines = []

    def lineReceived(self, line):
        self.lines.append(line)
        if not line:
            self.sendResponse()


    def lineReceived(self, line):
        self.lines.append(line)
        if not line:
            self.sendResponse()

    def sendResponse(self):
        self.sendLine(b"HTTP/1.1 200 OK")
        self.sendLine(b"")
        responseBody = b'You said:\r\n\r' + b'\r\n'.join(self.lines)
        self.transport.write(responseBody)
        self.transport.loseConnection()


class HTTPEchoFactory(protocol.ServerFactory):
    def buildProtocol(self, addr):
        return HTTPEchoProtocol()



reactor.listenTCP(10310, HTTPEchoFactory())
reactor.run()

    




