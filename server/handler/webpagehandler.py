import tornado.web
from tornado import gen
import server.debugger as logging
import os
import bcrypt
import concurrent.futures
# import MySQLdb
# import markdown
import os.path
import re
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)

# sample code
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/create", AuthCreateHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
        ]
        settings = dict(
            blog_title=u"Battle.ai",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules={"Entry": EntryModule},
            xsrf_cookies=True,
            # cookie_secret="secret_code",
            login_url="/auth/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        # self.db = torndb.Connection(
        #     host=options.mysql_host, database=options.mysql_database,
        #     user=options.mysql_user, password=options.mysql_password)

        self.maybe_create_tables()

    def maybe_create_tables(self):
        pass
        # try:
        #     self.db.get("SELECT COUNT(*) from entries;")
        # except MySQLdb.ProgrammingError:
        #     subprocess.check_call(['mysql',
        #                            '--host=' + options.mysql_host,
        #                            '--database=' + options.mysql_database,
        #                            '--user=' + options.mysql_user,
        #                            '--password=' + options.mysql_password],
        #                           stdin=open('schema.sql'))


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application

    def get_current_user(self):
        user_id = self.get_secure_cookie("blogdemo_user")
        if not user_id:
            return None
        return self.db.get("SELECT * FROM authors WHERE id = %s", int(user_id))

    def any_author_exists(self):
        return bool(self.db.get("SELECT * FROM authors LIMIT 1"))


class HomeHandler(BaseHandler):
    def get(self):
        print(self.db)
        self.render("main.html")


class MyPageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("sample.html")


class PlaygroundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


class EntryHandler(BaseHandler):
    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
        if not entry: raise tornado.web.HTTPError(404)
        self.render("entry.html", entry=entry)


class ArchiveHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC")
        self.render("archive.html", entries=entries)


class FeedHandler(BaseHandler):
    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY published "
                                "DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class ComposeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        entry = None
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
        self.render("compose.html", entry=entry)

    @tornado.web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            entry = self.db.get("SELECT * FROM entries WHERE id = %s", int(id))
            if not entry: raise tornado.web.HTTPError(404)
            slug = entry.slug
            self.db.execute(
                "UPDATE entries SET title = %s, markdown = %s, html = %s "
                "WHERE id = %s", title, text, html, int(id))
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())
            if not slug: slug = "entry"
            while True:
                e = self.db.get("SELECT * FROM entries WHERE slug = %s", slug)
                if not e: break
                slug += "-2"
            self.db.execute(
                "INSERT INTO entries (author_id,title,slug,markdown,html,"
                "published) VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP())",
                self.current_user.id, title, slug, text, html)
        self.redirect("/entry/" + slug)


class AuthCreateHandler(BaseHandler):
    def get(self):
        self.render("create_author.html")

    @gen.coroutine
    def post(self):
        if self.any_author_exists():
            raise tornado.web.HTTPError(400, "author already created")
        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt())
        author_id = self.db.execute(
            "INSERT INTO authors (email, name, hashed_password) "
            "VALUES (%s, %s, %s)",
            self.get_argument("email"), self.get_argument("name"),
            hashed_password)
        self.set_secure_cookie("blogdemo_user", str(author_id))
        self.redirect(self.get_argument("next", "/"))


class AuthLoginHandler(BaseHandler):
    def get(self):
        # If there are no authors, redirect to the account creation page.
        if not self.any_author_exists():
            self.redirect("/auth/create")
        else:
            self.render("login.html", error=None)

    @gen.coroutine
    def post(self):
        author = self.db.get("SELECT * FROM authors WHERE email = %s",
                             self.get_argument("email"))
        if not author:
            self.render("login.html", error="email not found")
            return
        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(author.hashed_password))
        if hashed_password == author.hashed_password:
            self.set_secure_cookie("blogdemo_user", str(author.id))
            self.redirect(self.get_argument("next", "/"))
        else:
            self.render("login.html", error="incorrect password")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blogdemo_user")
        self.redirect(self.get_argument("next", "/"))


class EntryModule(tornado.web.UIModule):
    def render(self, entry):
        return self.render_string("modules/entry.html", entry=entry)
