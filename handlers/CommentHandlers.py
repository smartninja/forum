import datetime
from handlers.BasicHandlers import BaseHandler
from google.appengine.api import users
from models.comment import Comment
from models.topic import Topic
from settings import ADMINS
from utils.decorators import user_required


class DeleteCommentHandler(BaseHandler):
    @user_required
    def get(self, comment_id):
        user = users.get_current_user().nickname()
        if user in ADMINS or user == Comment.get_by_id(int(comment_id)).author:
            args = {}
            self.base_args()
            self.render_template("delete.html", args)

    @user_required
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.deleted = True
        comment.put()

        topic = Topic.get_by_id(comment.the_topic_id)
        topic.num_comments -= 1
        topic.put()

        self.redirect("/topic/" + str(comment.the_topic_id))


class EditCommentHandler(BaseHandler):
    @user_required
    def get(self, comment_id):
        user = users.get_current_user()
        comment = Comment.get_by_id(int(comment_id))

        if user.nickname() in ADMINS or user.nickname() == comment.author:
            args = {}
            args["comment_content"] = comment.content
            self.base_args(user, args)
            self.render_template("edit-comment.html", args)
        else:
            self.redirect("/topic/" + str(comment.the_topic_id))

    @user_required
    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.content = self.request.get("content")
        comment.updated = datetime.datetime.now()
        comment.updated_by = users.get_current_user().nickname()
        comment.put()

        self.redirect("/topic/" + str(comment.the_topic_id))