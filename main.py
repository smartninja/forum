import webapp2
from handlers.BasicHandlers.SearchHandler import SearchHandler
from handlers.BasicHandlers.MainHandler import MainHandler
from handlers.TopicHandlers.TopicHandler import TopicHandler
from handlers.TopicHandlers.NewTopicHandler import NewTopicHandler
from handlers.TopicHandlers.DeleteTopicHandler import DeleteTopicHandler
from handlers.TopicHandlers.EditTopicHandler import EditTopicHandler
from handlers.TopicHandlers.CloseTopicHandler import CloseTopicHandler
from handlers.CommentHandlers.DeleteCommentHandler import DeleteCommentHandler
from handlers.CommentHandlers.EditCommentHandler import EditCommentHandler
from handlers.TopicHandlers.OpenTopicHandler import OpenTopicHandler


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
    webapp2.Route("/open-topic/<topic_id:\d+>", OpenTopicHandler),
], debug=True)