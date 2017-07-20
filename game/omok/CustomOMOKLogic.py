from gamebase.client.LogicHandler import LogicHandler

from battle_player.base.string import *

BOARD = "board"


class CustomOMOKLogic(LogicHandler):

    def __init__(self):
        """
        Develop own your OMOK AI
        width and height are board's width and height
        empty place is represented integer 0
        and your color is represented by number 0 1 2 ...

        your color is set automatically.
        """
        self.width = 0
        self.height = 0
        self.my_color = 0

    def init_phase(self, msg_type, data):
        """
        :param msg_type:
        :param data:
        :param init_data: {"width": (Integer), "height": (Integer), "color": (Integer)}
        :return: None
        """
        self.width = data["width"]
        self.height = data["height"]
        self.my_color = data["color"]
        return msg_type, {RESPONSE: OK}

    def loop_phase(self, msg_type, data):
        """
        :param msg_type:
        :param data: message received from server
                        it consist of {"msg": -, "msg_type": -, "data": { }}
        :return: return value is output sending data.
                    in this game,
                    if you want to put omok stone at board[x][y],
                    output is ...    dict -  { x: n, y: m }
        """
        print(data)
        board = data[BOARD]

        for x in range(self.width):
            for y in range(self.height):
                if board[x][y] == 0:
                    return msg_type, {"x": x, "y": y}
