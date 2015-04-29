from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
import datetime
from models.topic import Topic
from settings import ADMINS


class EditTopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user()
        if user.nickname() in ADMINS or user.nickname() == Topic.get_by_id(int(topic_id)).author:
            args = {}
            args["topic_title"] = Topic.get_by_id(int(topic_id)).title
            args["topic_content"]  = Topic.get_by_id(int(topic_id)).content
            args["tags"] = Topic.get_by_id(int(topic_id)).tags
            args["username"] = user.nickname()


            self.render_template("edit-topic.html", args)

    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.title = self.request.get("title")
        topic.content = self.request.get("content")
        topic.tags = self.request.get("all-tags").split(",")
        topic.updated = datetime.datetime.now()
        topic.updated_by = users.get_current_user().nickname()
        topic.put()

        self.redirect("/topic/" + str(topic_id))