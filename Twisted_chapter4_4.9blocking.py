from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import time

class BusyPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        time.sleep(5)
        return b"Finally done, at %s" % (time.asctime().encode('ascii'))

factory = Site(BusyPage())
reactor.listenTCP(10310, factory)
reactor.run()