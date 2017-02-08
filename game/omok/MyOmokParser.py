from game.omok.OmokParser import OmokParser

import game.debugger as logging

class MyOmokParser(OmokParser):
    def __init__(self):
        '''
        Develop own your omok AI
        width and height are board's width and height
        empty place is represented integer 0
        and your color is represented by number 0 1 2 ...

        your color is set automatically.
        '''
        self.width = 0
        self.height = 0
        self.my_color = 0
        pass

    def init_phase(self, init_data):
        """

        :param init_data: {"width": (Integer), "height": (Integer), "color": (Integer)}
        :return: None
        """
        self.width = init_data["width"]
        self.height = init_data["height"]
        self.my_color = init_data["color"]
        pass

    def loop_phase(self, board):
        """
        :param board: 2 dimension array that have omok board information
        :return: return value is output sending data.
                    in this game,
                    if you want to put omok stone at board[x][y],
                    output is ...    dict -  { x: n, y: m }
        """

        for x in range(self.width):
            for y in range(self.height):
                if board[x][y] == 0:
                    return {"x": x, "y": y}

