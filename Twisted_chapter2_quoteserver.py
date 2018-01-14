from twisted.internet.protocol import Factory
from twisted.internet import reactor, protocol

class QuoteProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numConnections +=1

    def dataReceived(self, data):
        print(f"Number of connections received: %d" % (self.factory.numConnections,))
        print(f"> Received: ``%s''\n> Sending: ``%s''" % (data, self.getQuote()))
        self.transport.write(self.getQuote())
        self.updateQuote(data)

    def connectionLost(self, reason):
        self.factory.numConnections -= 1

    def getQuote(self):
        return self.factory.quote

    def updateQuote(self, quote):
        self.factory.quote = quote


class QuoteFactory(Factory):
    numConnections = 0

    def __init__(self, quote=None):
        self.quote = quote or (b"An apple a day keeps the doctor away")

    def buildProtocol(self, addr):
        return QuoteProtocol(self)

reactor.listenTCP(10310, QuoteFactory())
reactor.run()

