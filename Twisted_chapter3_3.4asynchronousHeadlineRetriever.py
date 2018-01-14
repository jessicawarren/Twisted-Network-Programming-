from twisted.internet import reactor, defer
from twisted.logger import globalLogBeginner, textFileLogObserver
import sys

class HeadlineRetriever(object):
    def processHeadline(self, headline):
        if len(headline) > 50:
            self.d.errback(
                "The headline ''%s'' is too long!" % (headline,))
        else:
            self.d.callback(headline)

    def _toHTML(self, result):
        return "<h1>%s</h1>" % (result,)

    def getHeadline(self, input):
        self.d = defer.Deferred()
        reactor.callLater(1, self.processHeadline, input)
        self.d.addCallback(self._toHTML)
        return self.d

    def printData(self, result):
        print(result)
        reactor.stop()

    def printError(self, failure):
        print(failure)
        reactor.stop()


globalLogBeginner.beginLoggingTo([textFileLogObserver(sys.stdout)])

h = HeadlineRetriever()
d = h.getHeadline("Breaking News: Twisted Takes Us to the Moon!")
d.addCallbacks(h.printData, h.printError)
print("testing")
reactor.run()