from handlers.BasicHandlers.BaseHandler import BaseHandler
from models.comment import Comment
from models.topic import Topic
from google.appengine.api import users
from settings import ADMINS


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user()

        args = {}
        topic = Topic.get_by_id(int(topic_id))
        args["topic"] = topic
        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
            if user.nickname() in ADMINS:
                args["admin"]=True
        else:
            args["login"] = users.create_login_url("/")
        args["comments"] = Comment.query(Comment.deleted==False, Comment.the_topic_id==int(topic_id)).order(Comment.created).fetch()


        self.render_template("topic.html", args)

    def post(self, topic_id):
        author = users.get_current_user().nickname()
        content = self.request.get("content")

        if content:
            comment = Comment.create(author, content, int(topic_id))
            topic = Topic.add_comment(int(topic_id), comment.created, comment.author)

            self.redirect("/topic/" + str(topic_id))
