#!/bin/python3
# 2022.07.27
# chessMove.py

"""
Class for the different moves that can be made.

begin -- where the piece starts
end -- where the piece ends
"""

from typedefs import Coord


class Move:
    """Base class for all moves"""

    def __init__(self, begin: Coord, end: Coord):
        self.begin = begin
        self.end = end

    def __str__(self):
        return f"Piece moves from {self.begin} to {self.end}"


class Capture(Move):
    """A capture of another piece"""

    def __str__(self):
        return super().__str__() + " as a capture."


class EnPassant(Capture):
    """A capture via en passant"""

    def __str__(self):
        return super().__str__() + " as an en passant capture."


class PawnPush(Move):
    """A pawn movement"""

    def __str__(self):
        return super().__str__() + " as a pawn push."


class PawnDoublePush(PawnPush):
    """A pawn movement of 2 squares"""

    def __str__(self):
        return super().__str__() + " as a pawn double push."


class PawnPromotion(PawnPush):
    """A pawn promotion, whether by push or capture"""

    def __str__(self):
        return super().__str__() + " as a pawn promotion."


class Castle(Move):
    """Castling either king-side or queen-side"""

    def __str__(self):
        return super().__str__() + ' as in castling '
