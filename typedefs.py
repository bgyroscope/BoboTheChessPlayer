from __future__ import annotations

from enum import Enum


class PieceChar(Enum):
    """FEN characters for each piece"""

    KING = 'k'
    QUEEN = 'q'
    BISHOP = 'b'
    KNIGHT = 'n'
    ROOK = 'r'
    PAWN = 'p'

    def __str__(self):
        pieceNames = {
            PieceChar.KING: 'king',
            PieceChar.QUEEN: 'queen',
            PieceChar.BISHOP: 'bishop',
            PieceChar.KNIGHT: 'knight',
            PieceChar.ROOK: 'rook',
            PieceChar.PAWN: 'pawn'
        }
        return pieceNames[self]


class ColorChar(Enum):
    """FEN characters for the piece colors"""

    WHITE = 'w'
    BLACK = 'b'

    @property
    def opponent(self) -> ColorChar:
        """Returns this color's opposing color"""

        return ColorChar.BLACK if self == ColorChar.WHITE else ColorChar.WHITE

    def __str__(self):
        colorNames = {
            ColorChar.WHITE: 'white',
            ColorChar.BLACK: 'black'
        }
        return colorNames[self]

class Outcome(Enum): 
    WHITE_WINS = (1.0, 0.0)
    BLACK_WINS = (0,0, 1.0) 
    DRAW = (0.5, 0.5) 

    def __str__(self): 
        outcomeNames = { 
            Outcome.WHITE_WINS: 'White is victorious',
            Outcome.BLACK_WINS: 'Black is victorious',
            Outcome.DRAW: 'Draw.' 
        }
        return outcomeNames[self] 


class PositionStatus(Enum): 
    """ integer that represents the current status. result is a tuple expreses the result of the game """  
    INVALID =  -1            # Result.INVALID.value     
    IN_PLAY    = 0           # Result.IN_PLAY.value 
    WHITE_WINS = 1           # Result.WHITE_WINS.value
    BLACK_WINS = 2           # Result.BLACK_WINS.value
    STALEMATE  = 3           # (0.5,0.5) # Result.DRAW.value
    FIFTY_MOVE_DRAW = 4      # Result.DRAW.value
    THREEFOLD_DRAW  = 5      # (0.5,0.7) # Result.DRAW.value  
    INSUFFICIENT_DRAW = 6    # (0.5,0.5) # Result.DRAW.value

    def __str__(self):
        statusNames = {
            PositionStatus.INVALID : 'invalid', 
            PositionStatus.IN_PLAY    : 'Game is on going' , 
            PositionStatus.WHITE_WINS : 'White is victorious', 
            PositionStatus.BLACK_WINS : 'Black is victorious', 
            PositionStatus.STALEMATE  : 'Draw by stalemate' , 
            PositionStatus.FIFTY_MOVE_DRAW : 'Draw by fifty move rule.' , 
            PositionStatus.THREEFOLD_DRAW  : 'Draw by threefold repetition. '  , 
            PositionStatus.INSUFFICIENT_DRAW : 'Draw by insufficient material' 
        }
        return statusNames[self]


    @property
    def result(self) -> (tuple[float,float] | None): 
        whiteWins = Outcome.WHITE_WINS
        blackWins = Outcome.BLACK_WINS
        draw = Outcome.DRAW 

        # whiteWins = (1.0, 0.0) # Outcome.WHITE_WINS
        # blackWins = (0.0, 1.0) # Outcome.BLACK_WINS
        # draw = (0.5, 0.5)      # Outcome.DRAW 


        result = {
            PositionStatus.INVALID : None,
            PositionStatus.IN_PLAY    : None,
            PositionStatus.WHITE_WINS : whiteWins,
            PositionStatus.BLACK_WINS : blackWins, 
            PositionStatus.STALEMATE  : draw, 
            PositionStatus.FIFTY_MOVE_DRAW : draw,  
            PositionStatus.THREEFOLD_DRAW  : draw,  
            PositionStatus.INSUFFICIENT_DRAW : draw 
        }
        return result[self] 
 

ColorRGB = tuple[int, int, int]
"""A color represented by a (red, green, blue) tuple"""

ColorRGBA = tuple[int, int, int, int]
"""A color represented by a (red, green, blue, alpha) tuple"""

Color = (ColorRGB | ColorRGBA)

Coord = tuple[int, int]
"""An (x, y) coordinate pair"""

Vector = tuple[int, int]
"""A 2-tuple meant to represent a direction"""
