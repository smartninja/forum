import webapp2
from handlers import MainHandler, PostHandler, NewTopicHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/topic/<topic_id:\d+>", PostHandler),
    webapp2.Route("/new-topic", NewTopicHandler),
    #TODO- tag
], debug=True)