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
    

