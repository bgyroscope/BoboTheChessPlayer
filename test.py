#!/bin/python3
# 2022.12.12 
# Quick testing file. 

import pygame 

import gui.display as display
from gui.display import Display
from chessGame import Game
from chessBoardDisplay import Board

from typedefs import PieceChar, ColorChar, Coord

from chessPiece import (
    Piece,
    King,
    Queen,
    Bishop,
    Knight,
    Rook,
    Pawn
)


DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

initialFEN = "2k5/8/8/8/3b4/p6p/P6P/R3K2R w KQ - 8 13"      # castle examples 
initialFEN = "2kr4/8/8/2pP4/8/8/3K4/8 w - c6 0 2"    # testing check with ep case.  
initialFEN = "2kr4/8/8/2pP4/8/8/p2K3P/8 w - c6 0 2"    # testing check with ep case.  
initialFEN = "2kr4/7p/8/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # testing check with ep case.  

# Testing valid boards 
# initialFEN = "2kqr3/N6p/2K5/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # invalid because multiple kings
# initialFEN = "2kqr3/N6p/8/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # invalid because player not to move is in check. 
# initialFEN = "2kqr2P/7p/8/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # invalid of pawn placement 
# initialFEN = "2kqr2p/7p/8/2pP4/8/7b/p2K2PP/8 w - c6 0 2"    # invalid of pawn placement 
initialFEN = "2kqr3/7p/8/2pP4/8/7b/p2K2PP/p7 w - c6 0 2"    # invalid of pawn placement 
initialFEN = "2kqr3/7p/8/2pP4/8/7b/p2K2PP/P7 w - c6 0 2"    # invalid of pawn placement 

# initialFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kkq - 0 1'
initialFEN = 'rnbqkbnr/1ppp1pp1/8/p3p2p/P3P2P/8/1PPP1PP1/RNBQKBNR w KQkq - 0 1'   # after e4 e5, h4, h5, a4 a5




# initialFEN = "kr4K1/8/8/8/8/8/8/8 w - - 0 2"    # testing check move into and out of check. 
# initialFEN = "kr6/6K1/8/8/8/8/8/8 w - - 0 2"    # testing check move into and out of check. 


displayGame = True
displayGame = False

if not displayGame: 
    game = Game(initialFEN)
    
    print( game.toMove ) 
    # print( '\n further testing: \n',  game.getLegalMoves(game.toMove) )


    print( game.fenStr ) 
    for piece in ( King, Queen, Bishop, Knight, Pawn ): 
        helpdict = game.countPiece( piece ) 
        print( 'The number of white {} is {}, where as black is {}'.format(str(piece), helpdict[ColorChar.WHITE], helpdict[ColorChar.BLACK]  )  ) 


    print( game.getGameStatus() ) 


else: 

    print( initialFEN ) 

    #### test game play 
    window = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    game = Game(initialFEN)
    # game = Game()
    
    boardImage = display.loadImage('images/chess_board.png')
    piecesImage = display.loadImage('images/chess_pieces.png')
    board = Board(game, boardImage, piecesImage)
   

    print( 'Game status is: ', game.getGameStatus() ) 

    window.add(board, (0, 0))
    window.show()
    
    while window.state != display.QUIT:
        window.tick()
    
    pygame.quit()







