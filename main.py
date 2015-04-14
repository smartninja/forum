import webapp2
from handlers import MainHandler, PostHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/topic/<topic_id:\d+>", PostHandler)
], debug=True)