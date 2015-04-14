import webapp2
import os
import jinja2
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import Key


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        topics = db.GqlQuery("select * from Topic where deleted=False")
        args = {"topics":topics}
        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
        else:
            args["login"] = users.create_login_url("/")
        self.render_template("index.html", args)

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            t = Topic(title=title, content = content)
            t.put()
            self.redirect("/")

class PostHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user()
        if user:
            args = {}
            topic = Topic.get_by_id(int(topic_id))
            args["topic"] = topic
            args["user"] = user
            args["comments"] = topic.comments.order("created")
        self.render_template("topic.html", args)

    def post(self, topic_id):
        this_topic = Topic.get_by_id(int(topic_id))

        Comment(topic=this_topic,
                author = users.get_current_user().nickname(),
                content = self.request.get("content")).put()
        self.redirect("/topic/" + str(topic_id))





class Topic(db.Model):
    title = db.StringProperty()
    content = db.TextProperty()
    author = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True) #http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
    deleted = db.BooleanProperty(default=False)

class Comment(db.Model):
    topic = db.ReferenceProperty(Topic,
                                 collection_name="comments")
    author = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    content = db.TextProperty()
    deleted = db.BooleanProperty(default=False)