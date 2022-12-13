from typing import Generator

from typedefs import PieceChar, ColorChar, Coord
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

BoardGenerator = Generator[tuple[int, int, (Piece | None)], None, None]

STANDARD_START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w kqKQ - 0 1'


class Game:
    """Manages the game logic, such as moves, captures, win/loss, etc."""

    toMove: ColorChar
    castleRights: str
    epTarget: (Coord | None)
    halfMoveClock: int
    fullMoveNumber: int
    FENstr: str

    _board: list[list[(Piece | None)]]

    def __init__(self, startPos: str = STANDARD_START_POSITION):
        self.FENstr = startPos
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
        self.epTarget = FEN.squareToCoord(temp[3]) if temp[3] != '-' else None
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

    def enumerateBoard(self) -> BoardGenerator:
        """Generator of (row, col, piece) tuples"""

        for i, row in enumerate(self._board):
            for j, piece in enumerate(row):
                yield (i, j, piece)

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

    def getLegalMoves(self, color: ColorChar) -> list[Move]:
        """Returns a list of all legal moves for the player of the given color"""

        moves = []

        for row, col, piece in self.enumerateBoard():
            if piece is not None and piece.color == color:
                moves += self.getPieceLegalMoves(row, col)

        return moves

    def getPieceLegalMoves(self, row: int, col: int) -> list[Move]:
        """Returns a list of legal moves on the board for the piece at (row, col)"""

        piece = self._board[row][col]
        if piece is None:
            square = FEN.coordToSquare((row, col))
            raise Exception(f"No piece exists at {square}!")

        moves = self._getPiecePseudoLegalMoves(row, col, piece)
        moves += self._getPiecePseudoLegalCaptures(row, col, piece)
        moves += self._getPiecePseudoLegalSpecialStep(row, col, piece)   # to incorporate initial double step of pawn and castling

        # return moves

        # check that the moves are legal
        idxToRemove = [] 
        for idx, move in enumerate(moves): 
            if self.moveIntoCheck( move ): 
                idxToRemove.append(idx)     

        return [move for idx, move in enumerate(moves) if idx not in idxToRemove]  

        # now also consider castling, en passant, pawn promotion
        # also must check if a move puts the player in check


    def _getPiecePseudoLegalMoves(self, row: int, col: int, piece: Piece) -> list[Move]:
        moves = []
        start = (row, col)

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
                move = Move(start,end) 
                # if isinstance(piece, Pawn) and i == 2:
                #     move = PawnDoublePush(start, end)
                # else:
                #     move = Move(start, end)
                moves.append(move)

        return moves

    def _getPiecePseudoLegalCaptures(self, row: int, col: int, piece: Piece) -> list[Move]:
        captures = []
        start = (row, col)

        attacks = self._getPieceAttacks(row, col, piece)

        for newr, newc in attacks:
            target = self._board[newr][newc]
            end = (newr, newc)

            if target is not None:
                captures.append(Capture(start, end))

            # Check for en passant availability
            if isinstance(piece, Pawn) and end == self.epTarget:
                captures.append(EnPassant(start, end))

        return captures


    def _getPieceAttacks(self, row: int, col: int, piece: Piece) -> list[Coord]:
        attacks = []

        if piece.attackRange == chessPiece.MAX_RANGE:
            attackRange = self.numRows
        else:
            attackRange = piece.attackRange

        for attackDir in piece.attackDirection:
            for i in range(1, attackRange + 1):
                newr = row + attackDir[0] * i
                newc = col + attackDir[1] * i

                if self._coordOutOfBounds(newr, newc):
                    break

                attacks.append((newr, newc))

                # Stop after encountering another piece
                target = self._board[newr][newc]
                if target is not None:
                    # Ignore attacks on pieces of the same color
                    if target.color == piece.color:
                        attacks.pop()
                    break

        return attacks

    def _getPiecePseudoLegalSpecialStep(self, row: int, col: int, piece: Piece) -> list[Move]: 
        specialSteps = [] 
        start = (row, col) 

        if isinstance(piece, Pawn):   # or isinstance(piece, (Pawn,King) ): 

            for moveDir in piece.specialDirection:
                newr = row + moveDir[0] * piece.specialStep
                newc = col + moveDir[1] * piece.specialStep

                if self._coordOutOfBounds(newr, newc):
                    continue

                target = self._board[newr][newc]
                if target is not None:
                    continue

                end = (newr, newc)

                move = None
                if isinstance( piece, Pawn) and row == piece.homeRow: 
                    move = PawnDoublePush(start, end) 
                # elif isinstance( piece, King)  

                if move:
                    specialSteps.append(move)

        return specialSteps

    def isSquareAttacked(self, square: Coord, color: ColorChar) -> bool:
        """Returns whether the given square is attacked by a piece of the given color"""

        attacks: list[Coord] = []
        for row, col, piece in self.enumerateBoard():
            if piece is not None and piece.color == color:
                attacks += self._getPieceAttacks(row, col, piece)

        return square in attacks

    def executeMove(self, move: Move):
        """Performs the given move on the board"""

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
        # print( self.toMove, self.castleRights, self.epTarget, self.halfMoveClock, self.fullMoveNumber ) 


    def _updateState(self, move: Move):

        # Caslting rights  castleRights

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
        self.toMove = self.toMove.opponent()

        if self.toMove == ColorChar.WHITE:
            self.fullMoveNumber += 1

        self._updateFEN() 

    def _updateFEN(self): 
       
        tempBoardStr = self._getBoardStr()
        # to format the FEN correctly, convert enum to string
        toMoveStr = 'w' if self.toMove == ColorChar.WHITE else 'b'  
        epStr = '-' if not self.epTarget else FEN.coordToSquare( self.epTarget ) 

        self.FENstr = ' '.join( [tempBoardStr, toMoveStr, self.castleRights, epStr, str( self.halfMoveClock) , str( self.fullMoveNumber) ]  ) 

    def _getBoardStr(self):

        outstr = '' 
        for row in range(self.numRows): 
            j = 0 
            for col in range(self.numCols): 
                if self._board[row][col] == None: 
                    j += 1 
                else: 
                    if j!=0: 
                        outstr = outstr +  str(j)  + self._board[row][col].__str__() 
                    else: 
                        outstr = outstr + self._board[row][col].__str__() 
                    j = 0 

            if j != 0 : 
                outstr += str(j) 

            outstr += '/' 

        return outstr[:-1]    # remove accidentally over included '/'  

    def findKing(self, color: ColorChar) -> Coord:
        """Returns the position of the king of the given color"""

        for row, col, piece in self.enumerateBoard():
            if isinstance(piece, King) and piece.color == color:
                return (row, col)

        raise Exception(f"No {color} king found!")

    def inCheck(self, color: ColorChar) -> bool:
        """Returns whether the player of the given color is in check"""

        kingPos = self.findKing(color)
        return self.isSquareAttacked(kingPos, color.opponent())

    def moveIntoCheck(self, move: Move) -> bool: 
        """Returns if the current move excuted would put the player toMove in check. """

        tempGame = Game( self.FENstr ) 
        tempGame.executeMove( move  )

        if not tempGame.inCheck( self.toMove ): 
            return False
        else: return True 


    # def updateFEN(self, move ): 
    #     ''' update the FEN after a move  
    #         move -- a move object or subclass of move object, the flags are within the move motion 
    #         eventually include a flags argument for special moves 
    #     ''' 
 
    #     tempBoardStr = self.getBoardStr() 
    #    
    #     # changes due to flags 
    #     # castling rights -- if castle change self.castleRights = '-'. Also must check for king or rook move (based on c)  
    #     r,c = gf.coorToNum( move.end ) 
    #     movedPiece = self.arr[r][c]
    #     # no more castling rights if the piece that moved (or castle but that should already be covered by king moved)  #  or isinstance( move, cm.Castle):
    #     if isinstance( movedPiece, cp.King) or isinstance(movedPiece, cp.Rook):
    #         if isinstance( movedPiece, cp.King ): 
    #             toRemove = 'kq'
    #         else:
    #             rbegin, cbegin = gf.coorToNum( move.begin) 
    #             if cbegin == 0: 
    #                 toRemove = 'q'
    #             elif cbegin == 7: 
    #                 toRemove = 'k' 

    #         if self.toMove == 'w': toRemove = toRemove.upper()   # make uppercase for white pieces  

    #         newCastleRights = '' 
    #         for char in self.castleRights: 
    #             if char not in toRemove: 
    #                 newCastleRights += char 

    #         self.castleRights = newCastleRights



    #     # ep rights
    #     if isinstance( move, cm.PawnTwoSquare ): 
    #         r,c = gf.coorToNum( move.end )
    #         if self.toMove == 'w':  # white is making the pawn move 
    #             self.epRights = gf.numToCoor( [r+1,c] ) 
    #         else: # black made the pawn move 
    #             self.epRights = gf.numToCoor( [r-1,c] ) 

    #     else: 
    #         self.epRights = '-'   # ep only applies for the first available move 

    #     # half move clock can be reset by pawn moves or capture.
    #     if isinstance( move, cm.PawnMove ) or isinstance(move, cm.Capture):  
    #         self.halfMoveClock = 0 
    #     else: 
    #         self.halfMoveClock += 1 


    #     # update whose move it is at the end ----------------------------
    #     if self.toMove == 'w': 
    #         self.toMove = 'b'
    #    
    #     else: 
    #         self.toMove = 'w' 
    #         self.fullMoveNumber += 1 


    #     self.FEN = ' '.join( [tempBoardStr, self.toMove, self.castleRights, self.epRights, str( self.halfMoveClock) , str( self.fullMoveNumber) ]  ) 




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

