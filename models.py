from google.appengine.ext import ndb

from libs import pytz


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty(indexed=False)
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
    tags = ndb.StringProperty(repeated=True)
    num_comments = ndb.IntegerProperty(default=0)
    updated = ndb.DateTimeProperty()
    latest_comment_created = ndb.DateTimeProperty(auto_now_add=True)
    latest_comment_author = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, title, content, author, tags):
        topic = cls(title = title, content = content, author = author, tags = tags, latest_comment_author = author)
        topic.put()
        return topic

    @classmethod
    def get_datetime(cls, datetime):
        local_timezone = pytz.timezone('Europe/Ljubljana')
        return pytz.utc.localize(datetime).astimezone(local_timezone)


class Comment(ndb.Model):
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.TextProperty(indexed=False)
    deleted = ndb.BooleanProperty(default=False)
    the_topic_id = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty()

    @classmethod
    def create(cls, author, content, topic_id):
        comment = cls(author = author, content = content, the_topic_id = topic_id)
        comment.put()
        return comment

    @classmethod
    def get_datetime(cls, datetime):
        local_timezone = pytz.timezone('Europe/Ljubljana')
        return pytz.utc.localize(datetime).astimezone(local_timezone)