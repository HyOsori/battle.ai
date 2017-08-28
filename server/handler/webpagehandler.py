from server.model.player import Player

import tornado.web
import bcrypt
import concurrent.futures
import tornado.escape
from tornado import gen
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
from bson.objectid import ObjectId

USER_COOKIE = "battle_player"

# A thread pool to be used for password hashing with bcrypt.
executor = concurrent.futures.ThreadPoolExecutor(2)


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie(USER_COOKIE)
        if not user_id:
            return None
        user_dict = self.db.users.find_one({"_id": ObjectId(user_id.decode())})
        user = self.dict_to_user(user_dict)
        return user

    @staticmethod
    def dict_to_user(dict_user):
        if dict_user is None:
            return None
        return Player(dict_user["name"], None)


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = self.get_current_user()
        if user is None:
            self.redirect("/")
        else:
            self.render("index.html")


class LoginPageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")


class LobbyPageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = self.get_current_user()
        if user is None:
            self.redirect("/")
        else:
            self.render("lobby.html")


class GamePageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        user = self.get_current_user()
        if user is None:
            self.redirect("/")
        else:
            self.render("game.html")


class MyPageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


class SignUpHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        print("AuthSignUpHandler post is called")
        name = self.get_argument("name")

        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            bcrypt.gensalt()
        )
        user = Player(name, hashed_password)
        users_colletion = self.db.users
        user_id = users_colletion.insert(user.__dict__)

        self.redirect("/lobby")


class SignInHandler(BaseHandler):
    @gen.coroutine
    def post(self, *args, **kwargs):
        name = self.get_argument("name")
        user_dict = self.db.users.find_one({"name": name})
        if not user_dict:
            self.redirect("/")

        password = self.get_argument("password")

        hashed_password = yield executor.submit(
            bcrypt.hashpw, tornado.escape.utf8(self.get_argument("password")),
            tornado.escape.utf8(user_dict["password"])
        )

        if user_dict["password"] == hashed_password:
            self.set_secure_cookie(USER_COOKIE, str(user_dict["_id"]))
            self.redirect("/lobby")
        else:
            self.redirect("/")


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie(USER_COOKIE)
        self.redirect("/")


class MatchHandler(BaseHandler):
    def post(self):
        result_dict = dict()
        match_type = self.get_body_argument("type")
        result_dict["type"] = match_type
        try:
            result_dict["players"] = self.get_body_argument("players")
        except:
            pass
        try:
            result_dict["_id"] = self.get_body_argument("_id")
        except:
            pass

        self.write(result_dict)
