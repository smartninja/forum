from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.comment import Comment
from models.topic import Topic
from settings import ADMINS


class DeleteCommentHandler(BaseHandler):
    def get(self, comment_id):
        user = users.get_current_user().nickname()
        if user in ADMINS or user == Comment.get_by_id(int(comment_id)).author:
            self.render_template("delete.html")

    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.deleted = True
        comment.put()

        topic = Topic.get_by_id(comment.the_topic_id)
        topic.num_comments -= 1
        topic.put()

        self.redirect("/topic/" + str(comment.the_topic_id))