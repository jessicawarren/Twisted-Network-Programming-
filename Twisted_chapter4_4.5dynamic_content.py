from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site

import time

class ClockPage(Resource):
    isLeaf = True
    def render_GET(self, request):
        return b"the local time is %s" % (time.ctime().encode('ascii'))


resource = ClockPage()
factory = Site(resource)
reactor.listenTCP(10310, factory)
reactor.run()