from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class ChatProtocol(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.name = None
        self.state = "REGISTER"

    def connectionMade(self):
        self.sendLine(b"What's Your Name?")

    def connectionLost(self, reason):
        if self.name in self.factory.users:
            del self.factory.users[self.name]
            self.broadcastMessage(
                (
                    "%s has left the channel." % (self.name.decode('ascii'),)
                ).encode('ascii')
            )

    def lineReceived(self, line):
        if self.state == "REGISTER":
            self.handle_REGISTER(line)
        else:
            self.handle_CHAT(line)

    def handle_REGISTER(self, name):
        if name in self.factory.users:
            self.sendLine(b"Name taken, please choose another.")
            return
        self.sendLine(
            (
                "welcome, %s!" % (name.decode('ascii'),)
            ).encode('ascii')
        )
        self.broadcastMessage(
            (
                "%s has joined the channel." % (name,)
            ).encode('ascii')
        )
        self.name = name
        self.factory.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = ("<%s> %s" % (
            self.name.decode('ascii'),
            message.decode('ascii'),
        )).encode('ascii')
        self.broadcastMessage(message)

    def broadcastMessage(self, message):
        for name, protocol in self.factory.users.items():
            if protocol != self:
                protocol.sendLine(message)


class ChatFactory(Factory):
    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return ChatProtocol(self)

reactor.listenTCP(10310, ChatFactory())
reactor.run()
