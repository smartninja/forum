
from google.appengine.api import users
import datetime
from handlers.BasicHandlers import BaseHandler
from models.comment import Comment
from models.topic import Topic
from settings import ADMINS
from utils.decorators import user_required, admin_required


class TopicHandler(BaseHandler):
    def get(self, topic_id):
        user = users.get_current_user()

        args = {}
        topic = Topic.get_by_id(int(topic_id))
        args["topic"] = topic
        if user:
            if user.nickname() in ADMINS:
                args["admin"]=True
        self.base_args(user, args)
        args["comments"] = Comment.query(Comment.deleted==False, Comment.the_topic_id==int(topic_id)).order(Comment.created).fetch()


        self.render_template("topic.html", args)

    def post(self, topic_id):
        author = users.get_current_user().nickname()
        content = self.request.get("content")

        if content:
            comment = Comment.create(author, content, int(topic_id))
            topic = Topic.add_comment(int(topic_id), comment.created, comment.author)

            self.redirect("/topic/" + str(topic_id))
        else:
            self.redirect('/topic/' + str(topic_id))


class NewTopicHandler(BaseHandler):
    @user_required
    def get(self):
        args = {}
        user = users.get_current_user()
        self.base_args(user, args)
        self.render_template("new-topic.html", args)

    @user_required
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
        else:
            self.redirect('/')

class EditTopicHandler(BaseHandler):
    @user_required
    def get(self, topic_id):
        user = users.get_current_user()
        if user.nickname() in ADMINS or user.nickname() == Topic.get_by_id(int(topic_id)).author:
            args = {}
            args["topic_title"] = Topic.get_by_id(int(topic_id)).title
            args["topic_content"]  = Topic.get_by_id(int(topic_id)).content
            args["tags"] = Topic.get_by_id(int(topic_id)).tags
            self.base_args(user, args)


            self.render_template("edit-topic.html", args)

    @user_required
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.title = self.request.get("title")
        topic.content = self.request.get("content")
        topic.tags = self.request.get("all-tags").split(",")
        topic.updated = datetime.datetime.now()
        topic.updated_by = users.get_current_user().nickname()
        topic.put()

        self.redirect("/topic/" + str(topic_id))

class CloseTopicHandler(BaseHandler):
    @admin_required
    def get(self, topic_id):
        user = users.get_current_user()
        args = {}
        self.base_args(user, args)
        self.render_template("close-topic.html", args)

    @admin_required
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.closed=True
        topic.put()
        self.redirect("/topic/" + topic_id)

class DeleteTopicHandler(BaseHandler):
    @user_required
    def get(self, topic_id):
        user = users.get_current_user()
        args = {}
        self.base_args(user, args)
        self.render_template("delete.html", args)

    @user_required
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.deleted = True
        topic.put()

        self.redirect("/")



class OpenTopicHandler(BaseHandler):
    @admin_required
    def get(self, topic_id):
        user = users.get_current_user()
        if user.nickname() in ADMINS or user.nickname() == Topic.get_by_id(int(topic_id)).author:
            args = {}
            self.base_args(user, args)
            self.render_template("open-topic.html", args)

    @admin_required
    def post(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        topic.closed=False
        topic.put()
        self.redirect("/topic/" + topic_id)



