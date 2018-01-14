from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import html

class FormPage(Resource):
    isLeaf = True

    def render_GET(self, request):
        return b"""
<html>
 <body>
   <form method = "POST">
   <input name = "form-field" type = "text"  />
   <input type = "submit" />
   </form>
   </body>
   </html>
"""

    def render_POST(self, request):
        print(request.args)
        print(html.escape)
        return b"""
<html>
  <body>You submitted: %s </body>
  </html>
 """ % request.args[b"form-field"][0]


  #  def test(self)
  #      return b"""
#<html>
  #  <body> Testing </body>
  #  </html>"""



factory = Site(FormPage())
reactor.listenTCP(10310, factory)
reactor.run()

