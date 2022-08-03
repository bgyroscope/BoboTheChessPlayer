#!/bin/python3
# 2022.07.27
# chessMove.py 

# Class for the different moves that can be made. There are subclasses for simple, captures, ep, promotion, 

# promotion will be handled by chaning the piece according to the flag. 
# castling will be done by a king move. 

# begin -- where the piece starts.  alphanumeric code
# end -- where the piece ends.   alphanumeric loc
# remove -- piece to remove. alphanumeric loc 
# addition -- piece to add to the board 


class Move: 
    def __init__(self, begin, end) : 
        self.begin = begin
        self.end = end

    def __repr__(self): 
        return "piece moves from {} to {} ".format( self.begin, self.end ) 


class Simple(Move): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)


class Capture(Move): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)

    def __repr__(self): 
        return super().__repr__() + ' as a capture. ' 

# Pawn move subclasses ----------------------------------------------------
class PawnMove(Move): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)


    def __repr__(self): 
        return super().__repr__()  

class PawnOneSquare(PawnMove): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)

    def __repr__(self): 
        return super().__repr__() + ' as a pawn one step advance. ' 


class PawnTwoSquare(PawnMove): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)


    def __repr__(self): 
        return super().__repr__() + ' as a pawn two step advance. ' 

class PawnEP(PawnMove): 
    def __init__(self, begin, end): 
        super().__init__(begin, end)

    def __repr__(self): 
        return super().__repr__() + ' as a pawn ep capture. ' 


    

   






