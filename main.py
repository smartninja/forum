import webapp2
from handlers import MainHandler, TopicHandler, NewTopicHandler, DeleteTopicHandler, DeleteCommentHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/topic/<topic_id:\d+>", TopicHandler),
    webapp2.Route("/new-topic", NewTopicHandler),
    webapp2.Route("/delete-topic/<topic_id:\d+>", DeleteTopicHandler),
    webapp2.Route("/delete-comment/<comment_id:\d+>", DeleteCommentHandler)
], debug=True)