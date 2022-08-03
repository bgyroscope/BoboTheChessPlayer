#!/bin/python

# 2022.07.28 making sure I am using github correctly. 
# 2022.07.26 test.py -- test the creations of the objects. 

import genFun as gf 
import chessBoard as cb
import chessPiece as cp 
import chessMove  as cm
import chessPlayer as cp

import random



# board = cb.Board( '1K6/8/8/4pP2/8/8/8/8 w - - 0 1' )    # only white king
# board = cb.Board( '1Q2k3/8/8/4pP2/8/8/8/8 w - - 0 1' )  # only black king    
# board = cb.Board( '1K2k3/8/8/4pP2/8/8/8/8 w - - 0 1' )  # one of each
board = cb.Board( '1K2k3/8/8/4pP2/8/8/8/8 w - - 0 1' )  # one of each
# board = cb.Board( '1K2k3/8/8/4pP2/8/8/8/K7 w - - 0 1' )  # too many
# board = cb.Board( '6PK/6PP/8/8/8/8/pp6/kp6 w - - 0 1' )  # no moves are possible 


# board = cb.Board( '8/8/8/4pP2/8/8/8/8 w - - 0 1' )  # one of each

# testing out my pawns 
# initialFEN = "rnbqkbnr/2pppp2/8/8/8/8/2PPPP2/RNBQKBNR/ w kqKQ - 0 1" 
# initialFEN = "8/p7/8/8/8/8/1P6/8/ w kqKQ e3 24 1" 
# initialFEN = "8/pppppppp/8/8/8/8/PPPPPPPP/8/ w kqKQ - 0 1" 

#  # # initial board 
# initialFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w kqKQ - 0 1" 

# initialFEN = "8/p7/8/3pP3/8/8/8/8/ w kqKQ d6 24 1"   # ep position 

initialFEN = "8/p6P/8/8/3pP3/8/3p4/8/ w kqKQ e3 24 1"   # ep position 


board = cb.Board( initialFEN  ) 


for i in range(3): 
    board.display() 
    print( board.FEN) 

    print(  board.toMove, board.castleRights, board.epRights, board.halfMoveClock, board.fullMoveNumber ) 


    possMoves = board.possibleMoves( board.toMove ) 
    for move in possMoves: 
        print(move) 
    
    board.executeMove( possMoves[3] ) 

# 
# board.display() 

# board = cb.Board( "8/8/5P2/8/4p3/8/8/8 w - - 2 2" )

# for j in range(6):  
# 
#     print( '\n -------------------------------------------------------------------------------- \n '  ) 
#     
#     print( board) 
#     board.display() 
#     
#     possMoves =  board.possibleMoves( board.toMove ) 
#     
#     for move in possMoves: 
#         print(move ) 
#     
#     
#     print( 'current state: ' , board.FEN ) 
#     status =  board.checkStatus( board.toMove, possMoves ) 
#     # if status == "in prog": 
#     if True:
#         randMove = random.choice( possMoves ) 
#         print( 'Random move is ', randMove ) 
#         board.executeMove( randMove ) 
#   
#     else: 
#         print( status ) 
#         break 


# board = cb.Board( '1K2k3/8/8/4pP2/8/8/8/8 w - - 0 1' )  # one of each
# board.display() 
# ben = cp.human( 'w' ) 
# 
# possMoves = board.possibleMoves( board.toMove  )
# move = ben.decideMove( board, possMoves ) 
# 
# board.executeMove( move ) 
# board.display() 


# print( 'number of white and black kings: ', board.findKings() ) 


