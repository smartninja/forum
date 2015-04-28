from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from settings import ADMINS


class DeleteTopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user().nickname()

        if user in ADMINS:
            self.render_template("delete.html")

    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.deleted = True
        topic.put()

        self.redirect("/")