
from google.appengine.api import users
import datetime
from emails.update import email_new_topic, email_new_comment
from handlers.BasicHandlers import BaseHandler
from models.comment import Comment
from models.topic import Topic
from models.user import User
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

            if user.email() in topic.subscribers:
                args["subscribed"] = True
        self.base_args(user, args)
        args["comments"] = Comment.query(Comment.deleted==False, Comment.the_topic_id==int(topic_id)).order(Comment.created).fetch()


        self.render_template("topic.html", args)

    def post(self, topic_id):
        user = users.get_current_user()
        author = user.nickname()
        content = self.request.get("content")

        post_comment = self.request.get("post-comment")
        subscribe_button = self.request.get("subscribe-button")

        if post_comment:
            if content:
                comment = Comment.create(author, content, int(topic_id))
                Topic.add_comment(int(topic_id), comment.created, comment.author)

                the_user = ""
                for usr in User.query(User.email == user.email()).fetch():
                    the_user = usr


                topic = Topic.get_by_id(int(topic_id))
                subscriber_query = topic.subscribers
                for email in subscriber_query:
                    if email != user.email(): # don't send email update to the author of the comment
                        email_new_comment(the_user.first_name, Topic.get_by_id(int(topic_id)).title, str(topic_id), email)

                self.redirect('/topic/' + str(topic_id))
            else:
                self.redirect('/topic/' + str(topic_id))

        elif subscribe_button:
            topic = Topic.get_by_id(int(topic_id))
            user = users.get_current_user()
            user_email = user.email()

            if user_email in topic.subscribers:
                topic.subscribers.remove(user_email)
            else:
                topic.subscribers.append(user_email)

            topic.put()
            self.redirect("/topic/" + str(topic_id))


class NewTopicHandler(BaseHandler):
    @user_required
    def get(self):
        args = {}
        user = users.get_current_user()

        instructors = User.query(User.is_instructor == True).fetch()
        args["instructors"] = instructors

        self.base_args(user, args)
        self.render_template("new-topic.html", args)

    @user_required
    def post(self):
        user = users.get_current_user()
        title = self.request.get("title")
        content = self.request.get("content")
        tags = self.request.get("all-tags").split(",")
        instructor = self.request.get("instructor")
        if instructor:
            tags.append(instructor)

        author = users.get_current_user().nickname()

        if title and content and tags:
            topic = Topic.create(title, content, author, tags)
            topic.subscribers.append(user.email())
            topic.put()
            self.redirect("/topic/" + str(topic.key.id()))

            the_users = User.query(User.receive_updates==True).fetch()

            for user in the_users:
                email = user.email
                if user.first_name is None:
                    first_name = ""
                else:
                    first_name = user.first_name

                if email != users.get_current_user().email():
                    email_new_topic(first_name, title, topic.key.id(), email)
        else:
            self.redirect('/')

class EditTopicHandler(BaseHandler):
    @user_required
    def get(self, topic_id):
        user = users.get_current_user()
        topic = Topic.get_by_id(int(topic_id))

        if user.nickname() in ADMINS or user.nickname() == topic.author:
            args = {}
            args["topic_title"] = topic.title
            args["topic_content"] = topic.content
            args["tags"] = topic.tags
            self.base_args(user, args)
            self.render_template("edit-topic.html", args)
        else:
            self.redirect('/topic/' + topic_id)

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
