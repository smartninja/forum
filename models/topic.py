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
    updated_by = ndb.StringProperty()
    latest_comment_created = ndb.DateTimeProperty(auto_now_add=True)
    latest_comment_author = ndb.StringProperty(indexed=False)

    @classmethod
    def create(cls, title, content, author, tags):
        topic = cls(title = title, content = content, author = author, tags = tags, latest_comment_author = author)
        topic.put()
        return topic

    @classmethod
    def add_comment(cls, id, lcc, lca):
        topic = Topic.get_by_id(id)
        topic.num_comments += 1
        topic.latest_comment_created = lcc
        topic.latest_comment_author = lca
        topic.put()

    @classmethod
    def get_datetime(cls, datetime):
        local_timezone = pytz.timezone('Europe/Ljubljana')
        return pytz.utc.localize(datetime).astimezone(local_timezone)