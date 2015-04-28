from handlers.BasicHandlers.BaseHandler import BaseHandler
from google.appengine.api import users
from models.topic import Topic


class SearchHandler(BaseHandler):
    def get(self):
        query = self.request.get("query")
        user = users.get_current_user().nickname()
        args = {}

        if user:
            args["username"] = user
        if query:
            args["query"] = query
            topics = Topic.query(Topic.tags == query, Topic.deleted == False).order(-Topic.latest_comment_created2).fetch()
            if topics:
                args["topics"] = topics
            self.render_template("search.html", args)
        else:
            self.render_template("search.html")

    def post(self):
        query = self.request.get("searchbox")
        self.redirect("search?query=" + str(query))