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
from __future__ import annotations
from typing import Sequence
from functools import partial

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface

from typedefs import (
    PieceChar,
    ColorChar,
    ColorRGBA,
    Coord,
    Size
)
from chessGamePlay import Game
from chessPosition import Position
from chessMove import PawnPromotion
from chessPlayer import Human

from gui.displayable import (
    Container,
    Solid,
    Image,
    Panel,
    Grid,
    Button,
    ImageButton
)

SQUARE_HOVER_COLOR = (192, 192, 0, 128)
SQUARE_SELECT_COLOR = (255, 255, 0, 128)
MOVE_HILIGHT_COLOR = (0, 192, 0, 128)
MOVE_HOVER_COLOR = (0, 255, 0, 128)


class Board(Container):
    """A chess board displayable"""

    _game: Game
    _position: Position
    _player: Human
    _panel: Panel
    _piecesImage: Image
    _cellSize: int
    _promoting: bool
    _hoveredSquare: (Coord | None)
    _selectedSquare: (Coord | None)

    def __init__(self,
                 game: Game,
                 boardImage: Image,
                 piecesImage: Image):
        super().__init__()

        self._game = game
        self._position = game.position
        # Assumes one of the players is a human player
        self._player = next(player
                            for player in game.players.values()
                            if isinstance(player, Human))

        width, height = boardImage.size
        self._panel = Panel(width, height, background=boardImage)
        self._addChild(self._panel)
        # Assumes square cells
        self._cellSize = height // self._position.numRows

        self._piecesImage = piecesImage

        self._promoting = False
        self._tempMove = None
        self._hoveredSquare = None
        self._selectedSquare = None

        self._promotionPopup = self._makePromotionPopup()

    def _getPieceSprite(self, piece: PieceChar, color: ColorChar) -> Image:
        pieceIndices = {
            PieceChar.KING: 0,
            PieceChar.QUEEN: 1,
            PieceChar.BISHOP: 2,
            PieceChar.KNIGHT: 3,
            PieceChar.ROOK: 4,
            PieceChar.PAWN: 5
        }
        x = pieceIndices[piece] * self._cellSize
        y = 0 if color == ColorChar.WHITE else self._cellSize
        rect = Rect(x, y, self._cellSize, self._cellSize)
        sprite = self._piecesImage.crop(rect)
        return sprite

    @property
    def size(self) -> Size:
        return self._panel.size

    def render(self) -> Surface:
        self._panel.clearChildren()

        # Pieces
        for row, col, piece in self._position.enumerateBoard():
            if piece is not None:
                sprite = self._getPieceSprite(piece.char, piece.color)
                location = (col * self._cellSize, row * self._cellSize)
                self._panel.add(sprite, location)

        # Promotion
        if self._promoting:
            selectedPiece = self._promotionPopup.selectedPiece
            if selectedPiece is not None:
                assert isinstance(self._tempMove, PawnPromotion)
                self._tempMove.toPiece = selectedPiece
                self._player.selectedMove = self._tempMove
                self._tempMove = None
                self._promoting = False
            else:
                width, height = self.size
                location = (width // 2, height // 2)
                self._panel.add(self._promotionPopup,
                                location, pivot=(0.5, 0.5))

        # Highlighted squares
        if self._selectedSquare is not None:
            row, col = self._selectedSquare
            self._highlightSquare(row, col, SQUARE_SELECT_COLOR)
            self._highlightMoves()
        elif self._hasFocus() and self._hoveredSquare is not None:
            row, col = self._hoveredSquare
            self._highlightSquare(row, col, SQUARE_HOVER_COLOR)

        # Highlight checks
        for color in [ColorChar.WHITE, ColorChar.BLACK]:
            if self._position.inCheck(color):
                row, col = self._position.findKing(color)
                self._highlightSquare(row, col, (255, 0, 0, 128))

        return super().render()

    def _highlightMoves(self):
        row, col = self._selectedSquare  # type: ignore
        moves = self._position.getPieceLegalMoves(row, col)
        for move in moves:
            row, col = move.end

            # darker highlight for hovered moves
            hovered = self._hasFocus() and self._hoveredSquare == (row, col)
            color = MOVE_HOVER_COLOR if hovered else MOVE_HILIGHT_COLOR

            self._highlightSquare(row, col, color)

    def _highlightSquare(self, row: int, col: int, color: ColorRGBA):
        highlight = Solid(self._cellSize, self._cellSize, color)
        x = col * self._cellSize
        y = row * self._cellSize
        self._panel.add(highlight, (x, y))

    def _makePromotionPopup(self) -> PromotionPopUp:
        color = self._position.toMove
        knightSprite = self._getPieceSprite(PieceChar.KNIGHT, color)
        bishopSprite = self._getPieceSprite(PieceChar.BISHOP, color)
        rookSprite = self._getPieceSprite(PieceChar.ROOK, color)
        queenSprite = self._getPieceSprite(PieceChar.QUEEN, color)
        popup = PromotionPopUp(knightSprite, bishopSprite,
                               rookSprite, queenSprite)
        return popup

    def handle(self, event: Event) -> bool:
        if super().handle(event):
            return True

        if not self._promoting:
            if event.type == pygame.MOUSEMOTION:
                self._onMouseMove(event)
                return True

            if event.type == pygame.MOUSEBUTTONUP:
                self._onMouseClick(event)
                return True

        return False

    def _onMouseMove(self, event: Event):
        mouseX, mouseY = event.pos
        coords = self._screenPosToCoord(mouseX, mouseY)
        self._hoveredSquare = coords

    def _onMouseClick(self, event: Event):
        mouseX, mouseY = event.pos
        coords = self._screenPosToCoord(mouseX, mouseY)

        if self._selectedSquare is None:
            piece = self._position.getPieceAt(coords[0], coords[1])
            if piece is not None and piece.color == self._position.toMove:
                self._selectedSquare = coords
        else:
            row, col = self._selectedSquare
            moves = self._position.getPieceLegalMoves(row, col)
            selectedMove = next(
                (move for move in moves if move.end == coords), None)
            if selectedMove is not None:
                if isinstance(selectedMove, PawnPromotion):
                    # add pop up here .... 
                    # select a piece with the pop up 
                    # that selects the promotion property toPiece


                    self._tempMove = selectedMove
                    self._promoting = True
                else:
                    self._player.selectedMove = selectedMove
            self._selectedSquare = None

    def _screenPosToCoord(self, x: int, y: int) -> Coord:
        col = x // self._cellSize
        row = y // self._cellSize
        return (row, col)

    def _hasFocus(self) -> bool:
        return pygame.mouse.get_focused()


class PromotionPopUp(Container):
    """The pop-up used for selecting the piece to promote to"""

    fillColor = (97, 183, 123)

    selectedPiece: (PieceChar | None)

    def __init__(self,
                 knightSprite: Image,
                 bishopSprite: Image,
                 rookSprite: Image,
                 queenSprite: Image):
        super().__init__()

        buttons = self._makeButtons(
            knightSprite, bishopSprite, rookSprite, queenSprite)
        self._grid = Grid(2, 2, buttons, spacing=10)

        width, height = self._grid.size
        self._addChild(Solid(width, height, self.fillColor))
        self._addChild(self._grid)

        self.selectedPiece = None

    def _makeButtons(self,
                     knightSprite: Image,
                     bishopSprite: Image,
                     rookSprite: Image,
                     queenSprite: Image) -> Sequence[Button]:
        buttons = []
        sprites = [knightSprite, bishopSprite, rookSprite, queenSprite]
        chars = [PieceChar.KNIGHT, PieceChar.BISHOP,
                 PieceChar.ROOK, PieceChar.QUEEN]
        for char, sprite in zip(chars, sprites):
            button = ImageButton(sprite,
                                 SQUARE_HOVER_COLOR,
                                 partial(self._setSelectedPiece, char))
            buttons.append(button)
        return buttons

    def _setSelectedPiece(self, piece: PieceChar):
        self.selectedPiece = piece

    @property
    def size(self) -> Size:
        return self._grid.size
