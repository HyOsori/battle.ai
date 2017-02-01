#-*-coding:utf-8-*-
import base64
import json
import sys
import zlib

sys.path.insert(0,'../')
from gamebase.client.AIParser import AIParser

class OmokParser(AIParser):
    def __init__(self):
        pass

    def loop_phase(self):
        """
        must override
        :return:
        """
        pass