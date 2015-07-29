import webapp2, os, jinja2, filters
from google.appengine.api import users
from models.topic import Topic
from models.user import User
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
            if user.nickname() in ADMINS:
                args["admin"] = True
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

            the_users = User.query(User.email == user.email()).fetch()
            if not the_users:
                User.create(user.email(), user.nickname() in ADMINS)

        if more and next_curs:
            args["next"] = next_curs.urlsafe()

        instructors = User.query(User.is_instructor == True).fetch()
        args["instructors"] = instructors

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
            self.render_template("search.html", args)

    def post(self):
        query = self.request.get("searchbox")
        self.redirect("search?query=" + str(query))


class EditUserHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        args = {}

        user_query = User.query(User.email == user.email()).fetch()
        user_id = ""
        user_first_name = ""
        user_last_name = ""
        user_updates = ""

        for the_user in user_query:
            user_id = the_user.key.id()
            user_first_name = the_user.first_name
            user_last_name = the_user.last_name
            user_updates = the_user.receive_updates


        args["first_name"] = user_first_name
        args["last_name"] = user_last_name
        args["is_checked"] = user_updates

        self.base_args(user, args)
        self.render_template("edit-user.html", args)

    def post(self):
        user = users.get_current_user()
        args = {}


        user_query = User.query(User.email == user.email()).fetch()
        user_id = ""
        for the_user in user_query:
            user_id = the_user.key.id()

        the_user = User.get_by_id(int(user_id))
        the_user.first_name = self.request.get("first-name")
        the_user.last_name = self.request.get("last-name")

        updates = self.request.get("updates")
        if updates == u'on':
            the_user.receive_updates = True
        else:
            the_user.receive_updates = False

        the_user.put()

        self.redirect("/")


class AddInstructorHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        args = {}

        self.base_args(user, args)
        self.render_template("add-instructor.html", args)

    def post(self):
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        email = self.request.get("email")
        slug = self.request.get("slug")

        if first_name and last_name and email and slug:
            check_user = User.query(User.email == email).fetch()

            if check_user:
                user_id = ""
                for this_user in check_user:
                    user_id = this_user.key.id()

                the_user = User.get_by_id(int(user_id))
                the_user.first_name = first_name
                the_user.last_name = last_name
                the_user.email = email
                the_user.slug = slug
                the_user.is_instructor = True
                the_user.put()


            else:
                the_user = User.create(email, False)
                the_user.first_name = first_name
                the_user.last_name = last_name
                the_user.slug = slug
                the_user.is_instructor = True
                the_user.put()

            self.redirect("/")

        else:
            self.redirect("/add-instructor")