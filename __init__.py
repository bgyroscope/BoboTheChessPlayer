# pylint: disable=invalid-name

#!/bin/python3
# 2022.07.28
# __init__.py

"""This is the main program that iniitializes the game.
"""

import pygame

import gui
from gui import Display
from chessGame import Game
from chessBoard import Board

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800


if __name__ == '__main__':
    window = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    game = Game()

    boardImage = gui.loadImage('images/chess_board.png')
    piecesImage = gui.loadImage('images/chess_pieces.png')
    board = Board(game, boardImage, piecesImage)

    window.add(board, (0, 0))
    window.show()

    while window.state != gui.QUIT:
        window.tick()

    pygame.quit()
