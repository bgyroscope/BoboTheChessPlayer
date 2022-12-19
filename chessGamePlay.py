
from typing import Iterator
from typedefs import ColorChar, PositionStatus, Outcome
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



class AI_Game: 
    """ handles the game play of a computer vs computer game """ 
    players: dict[ColorChar, Player]
    position: Position

    outcome:  (Outcome | None) 
    positionStatus = (PositionStatus | None ) 
    PGN: str 


    def __init__(self, 
                 whitePlayer: Player,
                 blackPlayer: Player,
                 startPos: str = STANDARD_START_POSITION):
        self.players = {
            ColorChar.WHITE: whitePlayer,
            ColorChar.BLACK: blackPlayer
        }
        self.position = Position(startPos)
        

    def playGame(self) -> tuple[(Outcome | None), (PositionStatus | None), (str | None)]: 
        """Function that plays out the game outcome and the PGN of the game."""  

        if self.position.getPositionStatus == PositionStatus.INVALID: 
            return (None, None) 

        self.PGN = '[FEN "{}"]\n'.format(self.position.fenStr)
       

        tempcount = 0
        tempcountLimit = 1000
        while self.position.getPositionStatus() == PositionStatus.IN_PLAY and tempcount < tempcountLimit :
            activePlayer = self.players[self.position.toMove]
            moves = self.position.getLegalMoves(self.position.toMove)
            nextMove  = activePlayer.decideMove(self.position, moves) 
           
            if self.position.toMove == ColorChar.WHITE: 
                self.PGN += ' {}.'.format(self.position.fullMoveNumber)  

            self.PGN += ' ' + self.position.moveToAlgebraic(nextMove) 
            self.position.executeMove(nextMove) 

            tempcount += 1


        if tempcount >= tempcountLimit: 
            print( 'Very Long Game') 
            print( self.PGN ) 


        positionStatus = self.position.getPositionStatus() 
        self.outcome = positionStatus.result
        self.positionStatus = positionStatus

        return ( self.outcome, self.positionStatus, self.PGN ) 

    def updateScore(self): 
        self.players[ColorChar.WHITE].score += self.outcome.value[ColorChar.WHITE]   
        self.players[ColorChar.BLACK].score += self.outcome.value[ColorChar.BLACK]   


    def reset(self): 
        for player in players: 
            player.resetScore()  

