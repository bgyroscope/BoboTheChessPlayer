# pylint: disable=invalid-name

#!/bin/python3
# 2022.07.28
# __init__.py

"""This is the main program that iniitializes the game.
"""

import pygame

from typedefs import ColorChar
from chessGamePlay import Game
from chessPlayer import (
    Human,
    RandomComp
)
from chessBoardDisplay import Board

import gui.image
import gui.display
from gui.display import Display

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800


if __name__ == '__main__':
    window = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    user = Human(ColorChar.WHITE)
    comp = RandomComp(ColorChar.BLACK)
    game = Game(user, comp)

    boardImage = gui.image.loadImage('images/chess_board.png')
    piecesImage = gui.image.loadImage('images/chess_pieces.png')
    board = Board(game, boardImage, piecesImage)

    window.add(board, (0, 0))
    window.show()

    while window.state != gui.display.QUIT:
        game.update()
        window.tick()

    pygame.quit()
