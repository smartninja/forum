from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
    tags = ndb.StringProperty(repeated=True)
    num_comments = ndb.IntegerProperty()

class Comment(ndb.Model):
    author = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    content = ndb.TextProperty()
    deleted = ndb.BooleanProperty(default=False)
    the_topic_id = ndb.IntegerProperty()