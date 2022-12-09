#!/bin/python

# 2022.07.26
# chesspiece.py
"""
Defines the piece objects

Attributes:
  color --  'w' or 'b'
  direction -- array of directions it can move in row then in column direction.
  maxRange -- how far the piece can move in each of those directions
    ** special for pawns -- capDirection, capMaxRange for capture directions
"""

from typedefs import Vector

KING = 'k'
QUEEN = 'q'
BISHOP = 'b'
KNIGHT = 'n'
ROOK = 'r'
PAWN = 'p'

WHITE = 'w'
BLACK = 'b'

MAX_RANGE = -1


class Piece:
    """A generic chess piece
    """
    char: str
    color: str
    hasMoved: bool

    def __init__(self, char: str, color: str):
        """
        Args:
            char (str): the color of the piece ('w' or 'b')
            color (str): the FEN representation of the piece ('k', 'q', 'b', 'n', 'r', or 'p')
        """
        self.char = char.lower()
        self.color = color.lower()

        self.hasMoved = False

    @property
    def moveDirection(self) -> list[Vector]:
        """A list of directions the piece can move
        """
        raise NotImplementedError()

    @property
    def moveRange(self) -> int:
        """The maximum number of squares the piece can move
        """
        raise NotImplementedError()

    @property
    def captureDirection(self) -> list[Vector]:
        """A list of directions the piece can capture
        """
        return self.moveDirection

    @property
    def captureRange(self) -> int:
        """The maximum distance the piece can capture from
        """
        return self.moveRange

    def __str__(self) -> str:
        return self.char.lower() if self.color == BLACK else self.char.upper()


class Pawn(Piece):
    """A chess pawn
    """

    def __init__(self, color: str):
        super().__init__(PAWN, color)

    @property
    def moveDirection(self) -> list[Vector]:
        # a8 is (0, 0) so white pawns move in -y direction
        if self.color == WHITE:
            return [(-1, 0)]
        return [(1, 0)]

    @property
    def moveRange(self) -> int:
        return 2 if not self.hasMoved else 1

    @property
    def captureDirection(self) -> list[Vector]:
        if self.color == WHITE:
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]

    @property
    def captureRange(self) -> int:
        return 1


class Knight(Piece):
    """A chess knight
    """

    def __init__(self, color: str):
        super().__init__(KNIGHT, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(-1, 2), (1, 2), (2, 1), (2, -1),
                (1, -2), (-1, -2), (-2, -1), (-2, 1)]

    @property
    def moveRange(self) -> int:
        return 1


class Bishop(Piece):
    """A chess bishop
    """

    def __init__(self, color: str):
        super().__init__(BISHOP, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class Rook(Piece):
    """A chess rook
    """

    def __init__(self, color: str):
        super().__init__(ROOK, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class Queen(Piece):
    """A chess queen
    """

    def __init__(self, color: str):
        super().__init__(QUEEN, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1),
                (-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return MAX_RANGE


class King(Piece):
    """A chess king
    """

    def __init__(self, color: str):
        super().__init__(KING, color)

    @property
    def moveDirection(self) -> list[Vector]:
        return [(1, 1), (1, -1), (-1, -1), (-1, 1),
                (-1, 0), (1, 0), (0, -1), (0, 1)]

    @property
    def moveRange(self) -> int:
        return 1
