from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.topic import Topic
from settings import ADMINS


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        topics = Topic.query(Topic.deleted == False).order(-Topic.latest_comment_created2).fetch()
        args = {"topics": topics}

        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
            if user.nickname() in ADMINS:
                args["admin"] = True

        else:
            args["login"] = users.create_login_url("/")

        self.render_template("index.html", args)