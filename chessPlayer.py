#!/bin/python3
#
# 2022.07.28
# chessPlayer.py

"""
Class devoted to defining a player and the subclasses. It will include method for deciding moves.
"""

import random
from abc import ABC, abstractmethod

from typedefs import ColorChar
from chessPosition import Position
from chessMove import Move
from chessPiece import Piece

BoardArray = list[list[(Piece | None)]]


class Player(ABC):
    """Abstract class for a player that can select moves in a game of chess"""

    def __init__(self, color: ColorChar):
        self.color = color

    @abstractmethod
    def decideMove(self,
                   board: Position,
                   possMoves: list[Move]) -> (Move | None):
        """Starts the player's move decision process

        Args:
            board (BoardArray): the current board position
            possMoves (list[Move]): the list of available moves

        Returns:
            the selected move, or None if a move has not been decided on
        """

    def __str__(self):
        return f"{self.color} player"


class Human(Player):
    """A human player. Moves are selected by the user"""
    availableMoves: list[Move]
    selectedMove: (Move | None)

    def __init__(self, color: ColorChar):
        super().__init__(color)
        self.selectedMove = None

    def decideMove(self,
                   board: BoardArray,
                   possMoves: list[Move]) -> (Move | None):
        self.availableMoves = possMoves

        move = self.selectedMove
        if move is not None:
            self.selectedMove = None
        return move

    def __str__(self):
        return super().__str__() + " is human."


class RandomComp(Player):
    """A computer player that selects moves at random"""

    def decideMove(self,
                   board: BoardArray,
                   possMoves: list[Move]) -> (Move | None):
        return random.choice(possMoves)

    def __str__(self):
        return super().__str__() + " is random computer."
