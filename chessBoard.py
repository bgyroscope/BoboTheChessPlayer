#!/bin/python

# 2022.07.26
# chessboard.py
"""
Defines the Board object

Properties:
  FEN -- the Forsyth-Edwards Notation of the current position
  pos -- a set of all the FEN (minus castle rights, ep rights,
            half move clock and full move number) for three fold repetition
  arr -- board array None if empty, else a piece

Methods:
  init -- initialize from an FEN (default vaue is initial position)
  repr -- return FEN
  str --  same as rerpr
  display -- prints out the charArr of the board
"""

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from typedefs import (
    PieceChar,
    ColorChar,
    ColorRGBA,
    Point
)
from gui import Displayable, Image
from chessGame import Game
from chessPiece import Piece

SQUARE_HOVER_COLOR = (192, 192, 0, 128)
SQUARE_SELECT_COLOR = (255, 255, 0, 128)
MOVE_HILIGHT_COLOR = (0, 192, 0, 128)
MOVE_HOVER_COLOR = (0, 255, 0, 128)


class Board(Displayable):
    """A chess board displayable"""

    _game: Game
    _boardImage: Image
    _piecesImage: Image
    _cellSize: int
    _hoveredSquare: (Point | None)
    _selectedSquare: (Point | None)

    def __init__(self,
                 game: Game,
                 boardImage: Image,
                 piecesImage: Image):
        self._game = game

        self._boardImage = boardImage
        self._piecesImage = piecesImage
        _, height = self._boardImage.size()
        self._cellSize = height // self._game.numRows

        self._hoveredSquare = None
        self._selectedSquare = None

    def _getPieceSprite(self, piece: Piece) -> Surface:
        pieceIndices = {
            PieceChar.KING: 0,
            PieceChar.QUEEN: 1,
            PieceChar.BISHOP: 2,
            PieceChar.KNIGHT: 3,
            PieceChar.ROOK: 4,
            PieceChar.PAWN: 5
        }
        x = pieceIndices[piece.char] * self._cellSize
        y = 0 if piece.color == ColorChar.WHITE else self._cellSize
        rect = Rect(x, y, self._cellSize, self._cellSize)
        sprite = self._piecesImage.crop(rect)
        return sprite.render()

    def render(self) -> Surface:
        board = self._boardImage.render()

        # Pieces
        for i in range(self._game.numRows):
            for j in range(self._game.numCols):
                piece = self._game.getPieceAt(i, j)
                if piece is not None:
                    sprite = self._getPieceSprite(piece)
                    position = (j * self._cellSize, i * self._cellSize)
                    board.blit(sprite, position)

        # Highlighted squares
        if self._selectedSquare is not None:
            row, col = self._selectedSquare
            self._highlightSquare(board, row, col, SQUARE_SELECT_COLOR)
            self._highlightMoves(board)
        elif self._hasFocus() and self._hoveredSquare is not None:
            row, col = self._hoveredSquare
            self._highlightSquare(board, row, col, SQUARE_HOVER_COLOR)

        return board

    def _highlightMoves(self, board: Surface):
        row, col = self._selectedSquare  # type: ignore
        moves = self._game.getAvaiableMoves(row, col)
        for move in moves:
            row, col = move.end
            # darker highlight for hovered moves
            if self._hasFocus() and self._hoveredSquare == (row, col):
                color = MOVE_HOVER_COLOR
            else:
                color = MOVE_HILIGHT_COLOR
            self._highlightSquare(board, row, col, color)

    def _highlightSquare(self, board: Surface, row: int, col: int, color: ColorRGBA):
        highlight = Surface((self._cellSize, self._cellSize)).convert_alpha()
        highlight.fill(color)
        x = col * self._cellSize
        y = row * self._cellSize
        board.blit(highlight, (x, y, self._cellSize, self._cellSize))

    def handle(self, event: Event) -> bool:
        if event.type == pygame.MOUSEMOTION:
            self._onMouseMove(event)
            return True

        if event.type == pygame.MOUSEBUTTONUP:
            self._onMouseClick(event)
            return True

        return super().handle(event)

    def _onMouseMove(self, event: Event):
        mouseX, mouseY = event.pos
        coords = self._screenPosToSquare(mouseX, mouseY)
        self._hoveredSquare = coords

    def _onMouseClick(self, event: Event):
        mouseX, mouseY = event.pos
        coords = self._screenPosToSquare(mouseX, mouseY)

        if self._selectedSquare is None:
            piece = self._game.getPieceAt(coords[0], coords[1])
            if piece is not None and piece.color == self._game.toMove:
                self._selectedSquare = coords
        else:
            row, col = self._selectedSquare
            moves = self._game.getAvaiableMoves(row, col)
            selectedMove = next(
                (move for move in moves if move.end == coords), None)
            if selectedMove is not None:
                self._game.executeMove(selectedMove)
            self._selectedSquare = None

    def _screenPosToSquare(self, x: int, y: int) -> Point:
        col = x // self._cellSize
        row = y // self._cellSize
        return (row, col)

    def _hasFocus(self) -> bool:
        return pygame.mouse.get_focused()
