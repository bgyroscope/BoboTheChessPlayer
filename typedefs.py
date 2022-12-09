from enum import Enum


class PieceChar(Enum):
    """FEN characters for each piece"""
    KING = 'k'
    QUEEN = 'q'
    BISHOP = 'b'
    KNIGHT = 'n'
    ROOK = 'r'
    PAWN = 'p'


class ColorChar(Enum):
    """FEN characters for the piece colors"""
    WHITE = 'w'
    BLACK = 'b'


ColorRGB = tuple[int, int, int]
"""A color represented by a (red, green, blue) tuple"""
ColorRGBA = tuple[int, int, int, int]
"""A color represented by a (red, green, blue, alpha) tuple"""
Color = (ColorRGB | ColorRGBA)

Point = tuple[int, int]
"""An (x, y) coordinate pair"""
Vector = tuple[int, int]
"""A 2-tuple meant to represent a direction"""
