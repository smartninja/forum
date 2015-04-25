import webapp2
import os
import jinja2
from google.appengine.api import users
from settings import ADMINS
import filters

import datetime

from models.topic import Topic
from models.comment import Comment

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=False)
jinja_env.filters['markdown'] = filters.markitdown

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
        topics = Topic.query(Topic.deleted == False).order(-Topic.latest_comment_created).fetch()
        args = {"topics": topics}

        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
            if user.nickname() in ADMINS:
                args["admin"] = True

        else:
            args["login"] = users.create_login_url("/")

        self.render_template("index.html", args)


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


class DeleteCommentHandler(BaseHandler):
    def get(self, comment_id):
        user = users.get_current_user().nickname()
        if user in ADMINS or user == Comment.get_by_id(int(comment_id)).author:
            self.render_template("delete.html")

    def post(self, comment_id):
        comment = Comment.get_by_id(int(comment_id))
        comment.deleted = True
        comment.put()

        topic = Topic.get_by_id(comment.the_topic_id)
        topic.num_comments -= 1
        topic.put()

        self.redirect("/topic/" + str(comment.the_topic_id))

class EditTopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user().nickname()
        if user in ADMINS or user == Topic.get_by_id(int(topic_id)).author:
            args = {}
            args["topic_title"] = Topic.get_by_id(int(topic_id)).title
            args["topic_content"]  = Topic.get_by_id(int(topic_id)).content
            args["username"] = user
            self.render_template("edit-topic.html", args)

    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.title = self.request.get("title")
        topic.content = self.request.get("content")
        topic.updated = datetime.datetime.now()
        topic.updated_by = users.get_current_user().nickname()
        topic.put()

        self.redirect("/topic/" + str(topic_id))

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