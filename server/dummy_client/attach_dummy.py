from multi_dummy import DummyManager
from gameLogic.pixels.MyPixelsParser2 import MyPixelsParser2

dm = DummyManager(MyPixelsParser2)
dm.attach('127.0.0.1', 9001)


