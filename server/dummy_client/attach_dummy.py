from multi_dummy import DummyManager
from gameLogic.pixels.MyPixelsParser2 import MyPixelsParser2

import sys
sys.path.insert(0, "/home/bigs/battle.ai")

dm = DummyManager(MyPixelsParser2(), 'Dummy3')
dm.attach('127.0.0.1', 9001)


