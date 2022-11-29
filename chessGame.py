import pygame

import genFun as gf
from chessBoard import Board

SQUARE_HOVER_COLOR = (192, 192, 0, 128)
SQUARE_SELECT_COLOR = (255, 255, 0, 128)
MOVE_HILIGHT_COLOR = (0, 192, 0, 128)
MOVE_HOVER_COLOR = (0, 255, 0, 128)


class Game:
    def __init__(self, display, FEN='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w kqKQ - 0 1'):
        ''' 
        FEN - a Forsyth-Edwards Notation string
        '''
        self.display = display

        self.board = Board(FEN)

        self.hoveredSquare = None
        self.selectedSquare = None

        self.square = pygame.Surface((100, 100)).convert_alpha()

    def update(self):
        if self.selectedSquare is not None:
            row, col = self.selectedSquare
            self.moves = self.board.possibleMoves(row, col)
        else:
            self.moves = []

    def draw(self):
        board = self.board.render()
        self.display.blit(board, (0, 0))

        hovering = self.hoveredSquare is not None and pygame.mouse.get_focused()

        if self.selectedSquare is not None:
            row, col = self.selectedSquare
            self.highlightSquare(row, col, SQUARE_SELECT_COLOR)
            # highlight available moves
            for move in self.moves:
                row, col = gf.coorToNum(move.end)
                # darker highlight for hovered moves
                if hovering and self.hoveredSquare == (row, col):
                    color = MOVE_HOVER_COLOR
                else:
                    color = MOVE_HILIGHT_COLOR
                self.highlightSquare(row, col, color)
        elif hovering:
            row, col = self.hoveredSquare
            self.highlightSquare(row, col, SQUARE_HOVER_COLOR)

    def highlightSquare(self, row, col, color):
        s = 100
        self.square.fill(color)
        self.display.blit(self.square, (col * s, row * s, s, s))

    def event(self, ev):
        if ev.type == pygame.MOUSEMOTION:
            mouseX, mouseY = ev.pos
            col = mouseX // 100
            row = mouseY // 100
            self.hoveredSquare = (row, col)
        elif ev.type == pygame.MOUSEBUTTONUP:
            if self.selectedSquare is None:
                row, col = self.hoveredSquare
                piece = self.board.getPieceAt(row, col)
                if piece.color == self.board.toMove:
                    self.selectedSquare = self.hoveredSquare
            else:
                selectedMove = next((move for move in self.moves
                                     if gf.coorToNum(move.end) == self.hoveredSquare),None)
                if selectedMove is not None:
                    self.board.executeMove(selectedMove)
                self.selectedSquare = None
