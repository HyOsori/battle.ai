import json
import logging
import tornado.ioloop
import tornado.web
import tornado.websocket
from server.gameobject.room import Room

from server.handler.turngamehandler import TurnGameHandler
from server.string import *
from server.gameobject.user import Observer

class LobbyHandler(tornado.websocket.WebSocketHandler):
    pass

# log match chatting