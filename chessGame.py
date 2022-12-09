from typedefs import PieceChar, ColorChar, Point
import fen as FEN
from chessMove import (
    Move,
    Capture,
    EnPassant,
    PawnPush,
    PawnDoublePush
)
import chessPiece
from chessPiece import (
    Piece,
    King,
    Queen,
    Bishop,
    Knight,
    Rook,
    Pawn
)

STANDARD_START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ - 0 1'


class Game:
    """Manages the game logic, such as moves, captures, win/loss, etc.
    """
    toMove: ColorChar
    castleRights: str
    epTarget: (Point | None)
    halfMoveClock: int
    fullMoveNumber: int

    _board: list[list[(Piece | None)]]

    def __init__(self, startPos: str = STANDARD_START_POSITION):
        self.setState(startPos)

    def setState(self, fen: str):
        """Sets the game state from a Forsyth-Edwards Notation (FEN) string

        Args:
            fen (str): a FEN string describing the game state
        """
        temp = fen.split(' ')
        self.setPosition(temp[0])
        self.toMove = ColorChar(temp[1])
        self.castleRights = temp[2]
        self.epTarget = FEN.coordToNum(temp[3]) if temp[3] != '-' else None
        self.halfMoveClock = int(temp[4])
        self.fullMoveNumber = int(temp[5])

        # set for determining three fold repetition
        # self.pos = set()

    def setPosition(self, position: str):
        """Sets the position of pieces on the board

        Args:
            position (str): the board position in Forsyth-Edwards Notation
        """
        temp = position.split("/")

        self._board = []
        for i, row in enumerate(temp):
            self._board.append([])

            for char in row:
                if char in '12345678':
                    self._board[i] += [None] * int(char)
                else:
                    pieceChar = PieceChar(char.lower())
                    colorChar = ColorChar.BLACK if char.islower() else ColorChar.WHITE
                    piece = self._createPiece(pieceChar, colorChar)
                    self._board[i].append(piece)

    def _createPiece(self, pieceChar: PieceChar, colorChar: ColorChar) -> Piece:
        if pieceChar == PieceChar.KING:
            return King(colorChar)

        if pieceChar == PieceChar.QUEEN:
            return Queen(colorChar)

        if pieceChar == PieceChar.BISHOP:
            return Bishop(colorChar)

        if pieceChar == PieceChar.KNIGHT:
            return Knight(colorChar)

        if pieceChar == PieceChar.ROOK:
            return Rook(colorChar)

        return Pawn(colorChar)

    @property
    def numRows(self) -> int:  # pylint: disable=missing-function-docstring
        return len(self._board)

    @property
    def numCols(self) -> int:  # pylint: disable=missing-function-docstring
        if self.numRows == 0:
            return 0
        return len(self._board[0])

    def getPieceAt(self, row: int, col: int) -> (Piece | None):
        """Returns the piece at the given board position

        Args:
            row (int): the board row
            col (int): the board column

        Returns:
            (Piece | None): the piece at the given position (None if empty)
        """
        return self._board[row][col]

    def _coordOutOfBounds(self, row: int, col: int) -> bool:
        return row < 0 or row >= self.numRows or col < 0 or col >= self.numCols

    def getAvaiableMoves(self, row: int, col: int) -> list[Move]:
        """Returns a list of valid moves on the board for the piece at (row, col)
        """

        piece = self._board[row][col]
        if piece is None:
            return []

        moves = self._getPseudoLegalMoves(row, col)
        moves += self._getPseudoLegalCaptures(row, col)

        # now also consider castling, en passant, pawn promotion
        # also must check if a move puts the player in check

        return moves

    def _getPseudoLegalMoves(self, row: int, col: int) -> list[Move]:
        piece = self._board[row][col]
        if piece is None:
            return []

        moves = []
        begin = (row, col)

        if piece.moveRange == chessPiece.MAX_RANGE:
            moveRange = self.numRows
        else:
            moveRange = piece.moveRange

        for moveDir in piece.moveDirection:
            for i in range(1, moveRange + 1):
                newr = row + moveDir[0] * i
                newc = col + moveDir[1] * i

                if self._coordOutOfBounds(newr, newc):
                    break

                target = self._board[newr][newc]
                # Stop after encountering another piece
                if target is not None:
                    break

                end = (newr, newc)
                if isinstance(piece, Pawn) and i == 2:
                    move = PawnDoublePush(begin, end)
                else:
                    move = Move(begin, end)
                moves.append(move)

        return moves

    def _getPseudoLegalCaptures(self, row: int, col: int) -> list[Move]:
        piece = self._board[row][col]
        if piece is None:
            return []

        captures = []
        begin = (row, col)

        if piece.captureRange == chessPiece.MAX_RANGE:
            captureRange = self.numRows
        else:
            captureRange = piece.captureRange

        for capDir in piece.captureDirection:
            for i in range(1, captureRange + 1):
                newr = row + capDir[0] * i
                newc = col + capDir[1] * i

                if self._coordOutOfBounds(newr, newc):
                    break

                target = self._board[newr][newc]
                end = (newr, newc)

                # Stop after encountering another piece
                if target is not None:
                    if target.color != piece.color:
                        captures.append(Capture(begin, end))
                    break

                # Check for en passant availability
                if isinstance(piece, Pawn) and end == self.epTarget:
                    captures.append(EnPassant(begin, end))

        return captures

    def executeMove(self, move: Move):
        """Performs the given move on the board
        """
        startRow, startCol = move.begin
        endRow, endCol = move.end

        piece = self._board[startRow][startCol]
        if piece is None:
            return
        piece.hasMoved = True

        # Handles both moving & (normal) capturing
        self._board[endRow][endCol] = piece
        self._board[startRow][startCol] = None

        # En passant capturing
        if isinstance(move, EnPassant):
            # remove the captured pawn, whose location depends on color
            if self.toMove == ColorChar.WHITE:
                self._board[endRow + 1][endCol] = None
            else:
                self._board[endRow - 1][endCol] = None

        # Pawn promotion
        if isinstance(piece, Pawn) and \
                ((piece.color == ColorChar.WHITE and endRow == 0)
                 or (piece.color == ColorChar.BLACK and endRow == self.numRows - 1)):
            self._board[endRow][endCol] = Queen(piece.color)

        self._updateState(move)

    def _updateState(self, move: Move):
        # En passant availability
        if isinstance(move, PawnDoublePush):
            row, col = move.end
            if self.toMove == ColorChar.WHITE:
                self.epTarget = (row + 1, col)
            else:
                self.epTarget = (row - 1, col)
        else:
            self.epTarget = None

        # Half-move clock can be reset by pawn moves or capture
        if isinstance(move, (PawnPush, Capture)):
            self.halfMoveClock = 0
        else:
            self.halfMoveClock += 1

        # Current move + move number
        if self.toMove == ColorChar.BLACK:
            self.toMove = ColorChar.WHITE
            self.fullMoveNumber += 1
        else:
            self.toMove = ColorChar.BLACK

    # def checkStatus(self, color: str) -> str:
    #     """Determine the current status of the game

    #     Args:
    #         color (str): either 'b' or 'w'

    #     Returns:
    #         str: one of ['in prog', 'invalid', 'draw', 'checkmate']
    #     """

    #     # find the kings
    #     nw, nb = self.findKings()
    #     if nw == 0 and nb == 0 or nw > 1 or nb > 1:
    #         return "invalid"

    #     if nw == 1 and nb == 1:

    #         if not moveArr:
    #             moveArr = self.getAvaiableMoves(color)

    #         if moveArr == []:
    #             return "draw"
    #         else:
    #             return "in prog"

    #     else:
    #         if (color == 'w' and nw == 0) or (color == 'b' and nb == 0):
    #             return "checkmate"
    #         else:
    #             return "invalid"

    # def findKing(self, color: str) -> :
    #     ''' returns number of white then number of black kings '''
    #     nw = 0
    #     nb = 0

    #     for row in self._board:
    #         for p in row:
    #             if isinstance(p, King):
    #                 if p.color == 'w':
    #                     nw += 1
    #                 else:
    #                     nb += 1

    #     return (nw, nb)
