#!/bin/python3
#
# 2022.07.28
# chessPlayer.py

"""
Class devoted to defining a player and the subclasses. It will include method for deciding moves.
"""

import random
from abc import ABC, abstractmethod
from typing import Iterator

from typedefs import ColorChar
from chessPosition import Position
from chessMove import Move
from chessPiece import Piece

BoardArray = list[list[(Piece | None)]]


class Player(ABC):
    """Abstract class for a player that can select moves in a game of chess"""

    def __init__(self, nickname: str = 'unnamed'):
        self.nickname = nickname
        self.score = 0 

    @abstractmethod
    def decideMove(self,
                   board: Position,
                   possMoves: list[Move]) -> Iterator[(None | Move)]:
        """Starts the player's move decision process

        Args:
            board (BoardArray): the current board position
            possMoves (list[Move]): the list of available moves

        Yields:
            Iterator: yields None until a move has been decided on
        """

    def __str__(self):
        return "Player ({})".format(self.nickname) 


    def updateScore(self, pts: int): 
        self.score += pts 

    def resetScroe(self): 
        self.score = 0 

class Human(Player):
    """A human player. Moves are selected by the user"""
    availableMoves: list[Move]
    selectedMove: (Move | None)

    def __init__(self):
        super().__init__()
        self.selectedMove = None

    def decideMove(self,
                   board: BoardArray,
                   possMoves: list[Move]) -> Iterator[(None | Move)]:
        self.availableMoves = possMoves

        self.selectedMove = None
        while self.selectedMove is None:
            yield None
        yield self.selectedMove

    def __str__(self):
        return super().__str__() + " is human."


class RandomComp(Player):
    """A computer player that selects moves at random"""

    def decideMove(self,
                   board: BoardArray,
                   possMoves: list[Move]) -> Iterator[(None | Move)]:
        yield random.choice(possMoves)

    def __str__(self):
        return super().__str__() + " is random computer."
