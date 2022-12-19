from typedefs import ColorChar
from chessMove import Move
from chessPlayer import Player
from chessPosition import Position
from fen import STANDARD_START_POSITION


class Game:
    """Handles player decision logic"""

    players: dict[ColorChar, Player]
    position: Position

    _legalMoves: (list[Move] | None)

    def __init__(self,
                 whitePlayer: Player,
                 blackPlayer: Player,
                 startPos: str = STANDARD_START_POSITION):
        self.players = {
            ColorChar.WHITE: whitePlayer,
            ColorChar.BLACK: blackPlayer
        }
        self.position = Position(startPos)

        self._legalMoves = None

    def update(self):
        """Checks if the active player has selected
        their move, and if so, executes it
        """
        if self._legalMoves is None:
            self._legalMoves = self.position.getLegalMoves(self.position.toMove)

        activePlayer = self.players[self.position.toMove]
        move = activePlayer.decideMove(self.position, self._legalMoves)
        if move is not None:
            self.position.executeMove(move)
            self._legalMoves = None
