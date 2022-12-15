from typedefs import ColorChar
from typing import Iterator
from chessMove import (
    Move,
    Capture,
    EnPassant,
    PawnPush,
    PawnDoublePush,
    Castle
)



from chessPlayer import Player
from chessPosition import Position 
from fen import STANDARD_START_POSITION

class Game:  

    players: dict[ColorChar, Player]
    position: Position
    _moveQueue: (Iterator[(None | Move)] | None)


    def __init__(self,
                 whitePlayer: Player,
                 blackPlayer: Player,
                 startPos: str = STANDARD_START_POSITION):
        self.players = {
            ColorChar.WHITE: whitePlayer,
            ColorChar.BLACK: blackPlayer
        }
        self.position = Position(startPos)

        self._moveQueue = None

    def update(self):
        """Checks if the active player has selected
        their move, and if so, executes it
        """
        activePlayer = self.players[self.position.toMove]
        if self._moveQueue is None:
            position = self.position
            moves = self.position.getLegalMoves(self.position.toMove)
            self._moveQueue = activePlayer.decideMove(position, moves)

        move = next(self._moveQueue)
        if move is not None:
            self.position.executeMove(move)
            self._moveQueue = None



