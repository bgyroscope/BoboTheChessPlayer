#!/bin/python

# 2022.07.26 
# chesspiece.py  ---   defines the piece objects 
# 
# Attributes: 
#   loc -- location should be a alphanumeric coordinate, ie a1 or h8
#   color --  "w" or "b" 
#   direction -- array of directions it can move in specified by two integer arrays. 
#   maxRange -- how far the piece can move in each of those directions 
#       ** special for pawns -- capDirection, capMaxRange   for capture directions

import genFun as gf
import chessBoard as cb 


class Piece:

    colordict = { 'w': 'white', 'b': 'black' } 
    
    def __init__(self, loc, color ): 
        self.loc = loc      # location ie a1  
        self.color = color  # color of the piece. Either w or b  
        # for motion
        self.direction = [] 
        self.maxRange = 0

    def __repr__(self): 
        return "x" 

    def __str__(self): 
        return "x" 

    def getInfo(self): 
        return 'On {}, there is a {}'.format( self.loc, self.colordict[ self.color ]   ) 

class Pawn(Piece):

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
        if self.color == 'w': 
            self.direction = [ [-1,0] ]     # a8 is 0,0 so w pawns move in -y direction 
            # self.capDirection = [ [-1,-1], [-1,1] ] 
        else: 
            self.direction = [ [1,0] ] 
            # self.capDirection = [ [1,-1], [1, 1]  ]  

        self.maxRange = 1   # how far it can move forward usually 
        # self.capMaxRange = 1 

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

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
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

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
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

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
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

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
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

    def __init__(self, loc, color ): 
        super().__init__(loc,color)
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




def createPiece( char, loc  ): 
    if char == char.lower():   # lowercase 
        color = 'b' 
    else: 
        color = 'w' 


    char = char.lower() 

    if char == 'p': 
        return Pawn( loc, color )

    elif char == 'n': 
        return Knight( loc, color )  

    elif char == 'b': 
        return Bishop( loc, color )  

    elif char == 'r': 
        return Rook( loc, color )  

    elif char == 'q': 
        return Queen( loc, color )  

    elif char == 'k': 
        return King( loc, color )  



# 
# 
# 
# 
# 
# # subclasses below of each type of pieces 
# class Pawn(Piece):
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         if self.color == 'w': 
#             self.direction = [ [0,-1] ]     # a8 is 0,0 so w pawns move in -y direction 
#             self.capDirection = [ [-1,-1], [1,-1] ] 
#         else: 
#             self.direction = [ [0, 1] ] 
#             self.capDirection = [ [-1,1], [1, 1]  ]  
# 
#         self.maxRange = 1   # how far it can move forward usually 
#         self.capMaxRange = 1 
# 
#     def __repr__(self): 
#         return super().__repr__() + ' pawn' 
# 
# 
# class Knight(Piece): 
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         self.direction = [ [-1,2], [1,2], [2,1], [2,-1], [1,-2], [-1,-2], [-2,-1], [-2,1] ]
#         self.maxRange = 1   
# 
#     def __repr__(self): 
#         return super().__repr__() + ' knight'
# 
# 
# class Bishop(Piece): 
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         self.direction =[ [1,1], [1,-1], [-1,-1], [-1,1] ] 
#         self.maxRange = cb.Board.nrows -1  
# 
#     def __repr__(self): 
#         return super().__repr__() + ' bishop'
# 
# class Rook(Piece): 
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         self.direction = [ [-1,0], [1,0], [0,-1], [0,1] ] 
#         self.maxRange = cb.Board.nrows  -1
# 
# 
#     def __repr__(self): 
#         return super().__repr__() + ' rook'
# 
# 
# class Queen(Piece): 
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         self.direction = [ [1,1], [1,-1], [-1,-1], [-1,1], [-1,0], [1,0], [0,-1], [0,1] ]
#         self.maxRange = cb.Board.nrows - 1 
# 
# 
#     def __repr__(self): 
#         return super().__repr__() + ' queen'
# 
# 
# 
# class King(Piece): 
# 
#     def __init__(self, loc, color ): 
#         super().__init__(loc,color)
#         self.direction = [ [1,1], [1,-1], [-1,-1], [-1,1], [-1,0], [1,0], [0,-1], [0,1] ]
#         self.maxRange = 1   
# 
# 
#     def __repr__(self): 
#         return super().__repr__() + ' king'
# 
# 
# 
# 
# def createPiece( char, loc  ): 
#     if char == char.lower():   # lowercase 
#         color = 'b' 
#     else: 
#         color = 'w' 
# 
# 
#     char = char.lower() 
# 
#     if char == 'p': 
#         return Pawn( loc, color )
# 
#     elif char == 'n': 
#         return Knight( loc, color )  
# 
#     elif char == 'b': 
#         return Bishop( loc, color )  
# 
#     elif char == 'r': 
#         return Rook( loc, color )  
# 
#     elif char == 'q': 
#         return Queen( loc, color )  
# 
#     elif char == 'k': 
#         return King( loc, color )  
# 
# 
