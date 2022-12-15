#!/bin/python3
#
# 2022.07.28
# chessPlayer.py

"""
Class devoted to defining a player and the subclasses. It will include method for deciding moves.
"""

import random
from typing import Iterator

from typedefs import ColorChar
from chessPosition import Position
from chessMove import Move
from chessPiece import Piece

BoardArray = list[list[(Piece | None)]]


class Player:
    """Abstract class for a player that can select moves in a game of chess"""

    def __init__(self, color: ColorChar):
        self.color = color

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
        raise NotImplementedError(
            "Child class does not implement decideMove method")

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
                   possMoves: list[Move]) -> Iterator[(None | Move)]:
        self.availableMoves = possMoves
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
