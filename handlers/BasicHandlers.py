import webapp2, os, jinja2, filters
from google.appengine.api import users
from models.topic import Topic
from settings import ADMINS
from google.appengine.datastore.datastore_query import Cursor


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=False)
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

    def base_args(self, user, args): #username, logout/login
        if user:
            args["username"] = user.nickname()
            args["logout"] = users.create_logout_url("/")
        else:
            args["login"] = users.create_login_url("/")

        return args




class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        curs = Cursor(urlsafe=self.request.get('page'))
        topics, next_curs, more = Topic.query(Topic.deleted == False).order(-Topic.latest_comment_created2).fetch_page(50, start_cursor=curs)

        args = {"topics": topics}

        if user:
            if user.nickname() in ADMINS:
                args["admin"] = True

        if more and next_curs:
            args["next"] = next_curs.urlsafe()

        self.base_args(user, args)
        self.render_template("index.html", args)

class SearchHandler(BaseHandler):
    def get(self):
        query = self.request.get("query")
        user = users.get_current_user()
        args = {}

        self.base_args(user, args)

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