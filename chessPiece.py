#!/bin/python

# 2022.07.26 
# chesspiece.py  ---   defines the piece objects 
# 
# Attributes: 
#   color --  "w" or "b" 
#   direction -- array of directions it can move in row then in column direction.  
#   maxRange -- how far the piece can move in each of those directions 
#       ** special for pawns -- capDirection, capMaxRange   for capture directions

import genFun as gf
import chessBoard as cb 


class Piece:
    
    def __init__(self, color ): 
        self.color = color  # color of the piece. Either w or b  
        # for motion
        self.direction = [] 
        self.maxRange = 0

    def __repr__(self): 
        return "x" 

    def __str__(self): 
        return "x" 

    def getInfo(self): 
        return 'This is a {}'.format( gf.colordict[ self.color ]   ) 

class Pawn(Piece):

    def __init__(self, color ): 
        super().__init__(color)
        if self.color == 'w': 
            self.direction = [ [-1,0] ]     # a8 is 0,0 so w pawns move in -y direction 
            self.capDirection = [ [-1,-1], [-1,1] ] 
        else: 
            self.direction = [ [1,0] ] 
            self.capDirection = [ [1,-1], [1, 1]  ]  

        self.maxRange = 1   # how far it can move forward usually 

    def __repr__(self): 
        if self.color == 'w': 
            return 'P' 
        else: 
            return 'p' 

    def __str__(self): 
        if self.color == 'w': 
            return 'P' 
        else: 
            return 'p' 


    def getInfo(self): 
        return super().getInfo()  + ' pawn'





class Knight(Piece): 

    def __init__(self, color ): 
        super().__init__(color)
        self.direction = [ [-1,2], [1,2], [2,1], [2,-1], [1,-2], [-1,-2], [-2,-1], [-2,1] ]
        self.maxRange = 1   

    def __repr__(self): 
        if self.color == 'w': 
            return 'N' 
        else: 
            return 'n' 

    def __str__(self): 
        if self.color == 'w': 
            return 'N' 
        else: 
            return 'n' 


    def getInfo(self): 
        return super().getInfo()  + ' knight'


class Bishop(Piece): 

    def __init__(self, color ): 
        super().__init__(color)
        self.direction =[ [1,1], [1,-1], [-1,-1], [-1,1] ] 
        self.maxRange = cb.Board.nrows -1  

    def __repr__(self): 
        if self.color == 'w': 
            return 'B' 
        else: 
            return 'b' 

    def __str__(self): 
        if self.color == 'w': 
            return 'B' 
        else: 
            return 'b' 


    def getInfo(self): 
        return super().getInfo()  + ' bishop'




class Rook(Piece): 

    def __init__(self,  color ): 
        super().__init__(color)
        self.direction = [ [-1,0], [1,0], [0,-1], [0,1] ] 
        self.maxRange = cb.Board.nrows  -1

    def __repr__(self): 
        if self.color == 'w': 
            return 'R' 
        else: 
            return 'r' 

    def __str__(self): 
        if self.color == 'w': 
            return 'R' 
        else: 
            return 'r' 


    def getInfo(self): 
        return super().getInfo()  + ' rook'



class Queen(Piece): 

    def __init__(self,  color ): 
        super().__init__(color)
        self.direction = [ [1,1], [1,-1], [-1,-1], [-1,1], [-1,0], [1,0], [0,-1], [0,1] ]
        self.maxRange = cb.Board.nrows - 1 

    def __repr__(self): 
        if self.color == 'w': 
            return 'Q' 
        else: 
            return 'q' 

    def __str__(self): 
        if self.color == 'w': 
            return 'Q' 
        else: 
            return 'q' 


    def getInfo(self): 
        return super().getInfo()  + ' queen'



class King(Piece): 

    def __init__(self,  color ): 
        super().__init__(color)
        self.direction = [ [1,1], [1,-1], [-1,-1], [-1,1], [-1,0], [1,0], [0,-1], [0,1] ]
        self.maxRange = 1   

    def __repr__(self): 
        if self.color == 'w': 
            return 'K' 
        else: 
            return 'k' 

    def __str__(self): 
        if self.color == 'w': 
            return 'K' 
        else: 
            return 'k' 


    def getInfo(self): 
        return super().getInfo()  + ' king'




def createPiece( char  ): 
    if char == char.lower():   # lowercase 
        color = 'b' 
    else: 
        color = 'w' 


    char = char.lower() 

    if char == 'p': 
        return Pawn(  color )

    elif char == 'n': 
        return Knight(  color )  

    elif char == 'b': 
        return Bishop(  color )  

    elif char == 'r': 
        return Rook(  color )  

    elif char == 'q': 
        return Queen(  color )  

    elif char == 'k': 
        return King(  color )  



