from datetime import datetime
from twisted.web.util import redirectTo

def render_GET(self, request):
    return redirectTo(datetime.now().year, request)


## this is for an addition or override to 4.6