from google.appengine.ext import ndb


class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
    tags = ndb.StringProperty(repeated=True)
    num_comments = ndb.IntegerProperty(default=0)
    updated = ndb.DateTimeProperty()
    latest_comment_created = ndb.DateTimeProperty(indexed=False)
    latest_comment_author = ndb.StringProperty(indexed=False)

class Comment(ndb.Model):
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.TextProperty()
    deleted = ndb.BooleanProperty(default=False)
    the_topic_id = ndb.IntegerProperty()
    updated = ndb.DateTimeProperty()

    @classmethod
    def create(cls, author, content, topic_id):
        comment = cls(author = author, content = content, the_topic_id = topic_id)
        comment.put()
        return comment