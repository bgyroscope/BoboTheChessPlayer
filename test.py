#!/bin/python

# 2022.07.28 making sure I am using github correctly. 
# 2022.07.26 test.py -- test the creations of the objects. 

import chessBoard as cb
import chessPiece as cp 
import chessMove  as cm
import genFun as gf 

import random


# board = cb.Board( '8/2b2qqq/8/2R2B2/8/8/QQ6/1r6 w - - 0 1' ) 
board = cb.Board( '8/8/8/4pP2/8/8/8/8 w - - 0 1' ) 

board = cb.Board( "8/8/5P2/8/4p3/8/8/8 w - - 2 2" )

for j in range(6):  

    print( '\n -------------------------------------------------------------------------------- \n '  ) 
    
    print( board) 
    board.display() 
    
    possMoves =  board.possibleMoves( board.toMove ) 
    
    for move in possMoves: 
        print(move ) 
    
    
    print( 'current state: ' , board.FEN ) 
    randMove = random.choice( possMoves ) 
    print( 'Random move is ', randMove ) 
    board.executeMove( randMove ) 
    


# for piece in board.pieces: 
#     print( piece ) 
# 
# 
# for loc in [ 'h8', 'c5', 'e4', 'f2' ] : 
#     print( loc, board.isSquareEmpty(loc)  ) 



# board = cb.Board( '8/8/8/2P5/8/8/8/8 w - - 0 10' ) 
# board.display() 
# print( board ) 
# 
# 
# print( "my empty board" ) 
# board = cb.Board.createEmptyBoard()
# print( board ) 
# 
# 
# 
# print( '\n\n\n\n -------------------------------------------------------------------------------- \n '  ) 
# 
# piece1 = cp.Piece( 'a1', 'w' ) 
# print( piece1 ) 
# 
# piece2 = cp.Pawn( 'a2', 'b' ) 
# print( piece2 ) 
# print( piece2.getLoc() ) 
# 
# print( '\n\n\n\n -------------------------------------------------------------------------------- \n '  ) 
# print( '\n\n\n\n -------------------------------------------------------------------------------- \n '  ) 
# board = cb.Board.createEmptyBoard() 
# 
# # for loc in [ 'h8', 'c4', 'f2', 'a1' ]: 
# #     # piece1 = cp.King( loc, 'w' ) 
# #     # piece1 = cp.Knight( loc, 'w' ) 
# #     piece1 = cp.Bishop( loc, 'w' ) 
# #     print( piece1 ) 
# #     print( ) 
