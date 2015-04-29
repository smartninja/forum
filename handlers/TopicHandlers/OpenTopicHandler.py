import datetime
from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from settings import ADMINS


class OpenTopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user().nickname()
        if user in ADMINS:
            self.render_template("open-topic.html")

    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.closed=False
        topic.put()
        self.redirect("/topic/" + topic_id)