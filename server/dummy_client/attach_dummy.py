import sys
sys.path.insert(0, "/home/bigs/battle.ai/")

print sys.path

from multi_dummy import DummyManager
from gameLogic.pixels.MyPixelsParser2 import MyPixelsParser2

dm = DummyManager(MyPixelsParser2, 'Dummy3')
dm.attach('104.199.218.103', 9001)


