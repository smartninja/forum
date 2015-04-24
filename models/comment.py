from google.appengine.ext import ndb

from libs import pytz


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