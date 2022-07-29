#!/bin/python3 
# 
# 2022.07.28 
# chessPlayer.py 
# 
# Class devoted to defining a player and the subclasses. It will include method for deciding moves. 

import random 


class Player: 
    
    def __init__(self, color ) : 
        self.color = color 


    def __repr__ (self): 
        return "{} player ".format( self.color ) 

    def __str__ (self): 
        return "{} player ".format( self.color ) 





class Human(Player): 
    
    def __init__(self, color): 
        super().__init__(color)

    def __repr__ (self): 
        return super().__repr__() + " is human."  

    def __str__ (self): 
        return super().__repr__() + " is human."  


    def decideMove(self, board, possMoves):
        ''' method to decide which move to make. 
            board -- board object to consider 
            possMoves -- list of possible moves 
        
            return -- move object that is to be played
        '''

        # get raw string then check if valid move. 
        while True: 
            attemptMove = input( "Enter a move (should be letter then begining and end coordinate, e.g. Rh1-h8): ") 
            if len( attemptMove ) != 6: 
                print( "Please re-enter input." ) 

            else: 
                attemptBegin = attemptMove[1:3]
                attemptEnd   = attemptMove[4:6]

                for move in possMoves:
                    # for now don't bother checking the letter 
                    if move.begin == attemptBegin and move.end == attemptEnd: 
                        print( "Your move: ", move ) 
                        return move
            

class RandomComp(Player): 
    
    def __init__(self, color): 
        super().__init__(color)

    def __repr__ (self): 
        return super().__repr__() + " is random computer."  

    def __str__ (self): 
        return super().__repr__() + " is random computer."  


    def decideMove(self, board, possMoves):
        ''' method to decide which move to make. 
            board -- board object to consider 
            possMoves -- list of possible moves 
        
            return -- move object that is to be played
        '''

        return random.choice( possMoves ) 


