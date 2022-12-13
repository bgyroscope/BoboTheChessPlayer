#!/bin/python3
# 2022.12.12 
# Quick testing file. 

import pygame 

import gui
from gui import Display
from chessGame import Game
from chessBoard import Board

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

initialFEN = "2k5/8/8/8/3b4/p6p/P6P/R3K2R w KQ - 8 13"      # castle examples 
initialFEN = "2kr4/8/8/2pP4/8/8/3K4/8 w - c6 0 2"    # testing check with ep case.  
initialFEN = "2kr4/8/8/2pP4/8/8/p2K3P/8 w - c6 0 2"    # testing check with ep case.  


window = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)

game = Game(initialFEN)

boardImage = gui.loadImage('images/chess_board.png')
piecesImage = gui.loadImage('images/chess_pieces.png')
board = Board(game, boardImage, piecesImage)

window.add(board, (0, 0))
window.show()

while window.state != gui.QUIT:
    window.tick()

pygame.quit()







