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
initialFEN = "2kr4/7p/8/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # testing check with ep case.  


# initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kkq - 0 1'
initialFEN = 'rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQkq - 0 1'   # after e4 e5, h4, h5, a4 a5




# initialFEN = "kr4K1/8/8/8/8/8/8/8 w - - 0 2"    # testing check move into and out of check. 
# initialFEN = "kr6/6K1/8/8/8/8/8/8 w - - 0 2"    # testing check move into and out of check. 

displayGame = True


if not displayGame: 
    game = Game(initialFEN)
    
    print( game.toMove ) 
    print( '\n further testing: \n',  game.getLegalMoves(game.toMove) )


else: 

    print( initialFEN ) 

    #### test game play 
    window = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    game = Game(initialFEN)
    # game = Game()
    
    boardImage = gui.loadImage('images/chess_board.png')
    piecesImage = gui.loadImage('images/chess_pieces.png')
    board = Board(game, boardImage, piecesImage)
    
    window.add(board, (0, 0))
    window.show()
    
    while window.state != gui.QUIT:
        window.tick()
    
    pygame.quit()







