import webapp2
from handlers import MainHandler, TopicHandler, NewTopicHandler, \
    DeleteTopicHandler, DeleteCommentHandler, EditTopicHandler, EditCommentHandler, CloseTopicHandler, SearchHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route("/topic/<topic_id:\d+>", TopicHandler),
    webapp2.Route("/new-topic", NewTopicHandler),
    webapp2.Route("/delete-topic/<topic_id:\d+>", DeleteTopicHandler),
    webapp2.Route("/delete-comment/<comment_id:\d+>", DeleteCommentHandler),
    webapp2.Route("/edit-topic/<topic_id:\d+>", EditTopicHandler),
    webapp2.Route("/edit-comment/<comment_id:\d+>", EditCommentHandler),
    webapp2.Route("/close-topic/<topic_id:\d+>", CloseTopicHandler),
    webapp2.Route("/search", SearchHandler),
], debug=True)