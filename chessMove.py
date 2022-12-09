#!/bin/python3
# 2022.07.27
# chessMove.py

"""
Class for the different moves that can be made.
    There are subclasses for simple, captures, ep, promotion,

promotion will be handled by chaning the piece according to the flag.
castling will be done by a king move.

begin -- where the piece starts.  alphanumeric code
end -- where the piece ends.   alphanumeric loc
remove -- piece to remove. alphanumeric loc
addition -- piece to add to the board
"""


class Move:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"Piece moves from {self.begin} to {self.end}"


class Capture(Move):
    def __str__(self):
        return super().__str__() + ' as a capture.'


class EnPassant(Capture):
    def __str__(self):
        return super().__str__() + ' as an en passant capture.'


class PawnPush(Move):
    def __str__(self):
        return super().__str__() + ' as a pawn push.'


class PawnDoublePush(PawnPush):
    def __str__(self):
        return super().__str__() + ' as a pawn double push.'
