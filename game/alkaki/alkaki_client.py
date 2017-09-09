# -*-coding:utf-8-*-
from battle_player.base.Player import play
from game.alkaki.alkaki_logic import CustomAlkakiLogic


if __name__ == "__main__":
    logic = CustomAlkakiLogic()
    play(logic)

