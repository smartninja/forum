from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
import datetime
from models.comment import Comment
from settings import ADMINS


class EditCommentHandler(BaseHandler):
    def get(self, comment_id):
        user = users.get_current_user().nickname()
        if user in ADMINS or user == Comment.get_by_id(int(comment_id)).author:
            args = {}
            args["comment_content"] = Comment.get_by_id(int(comment_id)).content
            args["username"] = user
            self.render_template("edit-comment.html", args)

    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.content = self.request.get("content")
        comment.updated = datetime.datetime.now()
        comment.updated_by = users.get_current_user().nickname()
        comment.put()

        self.redirect("/topic/" + str(comment.the_topic_id))