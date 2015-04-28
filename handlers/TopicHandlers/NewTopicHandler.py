from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.topic import Topic


class NewTopicHandler(BaseHandler):
    def get(self):
        args = {}
        user = users.get_current_user()

        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
            self.render_template("new-topic.html", args)
        else:
            self.redirect("/")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")
        tags = self.request.get("all-tags").split(",")
        instructor = self.request.get("instructor")
        if instructor:
            tags.append(instructor)

        author = users.get_current_user().nickname()

        if title and content and tags:
            topic = Topic.create(title, content, author, tags)
            self.redirect("/topic/" + str(topic.key.id()))