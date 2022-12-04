#!/bin/python3
# 2022.07.28
# main.py 

# This is the main program that iniitializes the game. 

import genFun as gf 
import chessBoard as cb
import chessPiece as cp 
import chessMove  as cm
import chessPlayer as cp


# initialFEN = "rnbqkbnr/8/8/8/8/8/8/RNBQKBNR/ w kqKQ - 0 1" 
initialFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w kqKQ - 0 1" 


score = [ 0, 0] 
color1 = 'w'
color2 = 'b' 

toggleFirstGame = True

while True: 

    if toggleFirstGame: 
        toggleFirstGame = False
    else: 
        color1, color2 = color2, color1 
    

    # initilize the players 
    player1 =  cp.Human(color1) 
    player2 =  cp.RandomComp(color2) 
    
    
    board = cb.Board( initialFEN ) 
    
    print( 'player1: ' , player1 ) 
    print( 'player2: ' , player2 ) 
    
    
    while board.checkStatus(board.toMove) == "in prog": 
        
        board.display() 
        # possMoves = board.possibleMoves( board.toMove ) 
        validMoves = board.validMoves( board.toMove ) 
    
        if player1.color == board.toMove: 
            # move = player1.decideMove( board, possMoves )
            move = player1.decideMove( board, validMoves )
        else: # player2.color == board.toMove
            # move =  player2.decideMove( board, possMoves ) 
            move =  player2.decideMove( board, validMoves ) 
    
        board.executeMove( move ) 
    
        print( '\n' , move , '\n' ) 
    
    
    if board.checkStatus(board.toMove) == 'draw': 
        print( '\n\n It was a draw! \n\n ' ) 
        score[0] += 0.5
        score[1] += 0.5 
    
    elif board.checkStatus(board.toMove) == 'checkmate': 
    
        # who ever is to move lost. 
        if board.toMove == player1.color: 
            print( '\n\n Player2 was victorious! \n\n' ) 
            score[1] +=1 
        else: 
            print( '\n\n Player1 was victorious! \n\n' ) 
            score[0] +=1 
    
    
    print( 'Player1: ' ,  score[0] ,  ' vs Player2: ' , score[1] ) 
    
    
    while True: 
        yesOrNo = input( "Play again? (y or n): " )
        yesOrNo.lower() 
        if yesOrNo == 'y' or  yesOrNo == 'n': 
            break 
    
    
    if yesOrNo == 'n': 
        break



