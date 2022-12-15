#!/bin/python

# 2022.07.26
# chesspiece.py
"""
Defines the piece objects

Attributes:
  color --  'w' or 'b'
  homeRow -- 7 for white pieces (6 for pawn) and 0 for black pieces (1 for pawns)
  direction -- array of directions it can move in row then in column direction.
  maxRange -- how far the piece can move in each of those directions
    ** special for pawns -- capDirection, capMaxRange for capture directions
                            specialDirection, specialStep for initial double step
"""

from typedefs import (
    PieceChar,
    ColorChar,
    Vector
)


MAX_RANGE = -1


class Piece:
    """A generic chess piece"""

    char: PieceChar
    color: ColorChar
#     hasMoved: bool

    def __init__(self, char: PieceChar, color: ColorChar):
        """
        Args:
            char (str): the color of the piece ('w' or 'b')
            color (str): the FEN representation of the piece ('k', 'q', 'b', 'n', 'r', or 'p')
        """
        self.char = char
        self.color = color

        # self.hasMoved = False

    @property
    def homeRow(self) -> int:
        return 7 if self.color == ColorChar.WHITE else 0  # 7 for numRows-1


    @property
    def moveDirection(self) -> list[Vector]:
        """A list of directions the piece can move"""
        raise NotImplementedError("Child class does not implement moveDirection")

    @property
    def moveRange(self) -> int:
        """The maximum number of squares the piece can move"""
        raise NotImplementedError("Child class does not implement moveRange")

    @property
    def attackDirection(self) -> list[Vector]:
        """A list of directions the piece can capture"""
        return self.moveDirection

    @property
    def attackRange(self) -> int:
        """The maximum distance the piece can capture from"""
        return self.moveRange

    def __str__(self) -> str:
        char = self.char.value
        return char.lower() if self.color == ColorChar.BLACK else char.upper()


class Pawn(Piece):
    """A chess pawn"""

    @property
    def homeRow(self) -> int:
        return 6 if self.color == ColorChar.WHITE else 1

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.PAWN, color)

    @property
    def moveDirection(self) -> list[Vector]:
        # a8 is (0, 0) so white pawns move in -y direction
        if self.color == ColorChar.WHITE:
            return [(-1, 0)]
        return [(1, 0)]

    @property
    def moveRange(self) -> int:
        # return 2 if not self.hasMoved else 1
        return 1

    @property
    def attackDirection(self) -> list[Vector]:
        if self.color == ColorChar.WHITE:
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]

    @property
    def attackRange(self) -> int:
        return 1

    # special pawn properties-------------------- 
    @property 
    def specialStep(self) -> int:
        return 2

    @property 
    def specialDirection(self) -> list[Vector]: 
        return self.moveDirection 


class Knight(Piece):
    """A chess knight"""

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.KNIGHT, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(-1, 2), (1, 2), (2, 1), (2, -1),
                (1, -2), (-1, -2), (-2, -1), (-2, 1)]

    @property
    def moveRange(self) -> int:
        return 1


class Bishop(Piece):
    """A chess bishop"""

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.BISHOP, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class Rook(Piece):
    """A chess rook"""

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.ROOK, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class Queen(Piece):
    """A chess queen"""

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.QUEEN, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1),
                (-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class King(Piece):
    """A chess king"""

    def __init__(self, color: ColorChar):
        super().__init__(PieceChar.KING, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1),
                (-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return 1
