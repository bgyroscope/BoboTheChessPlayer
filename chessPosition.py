from typing import Iterator

from typedefs import PieceChar, ColorChar, PositionStatus, Outcome, Coord
import fen as FEN
from fen import STANDARD_START_POSITION
from chessMove import (
    Move,
    Capture,
    EnPassant,
    PawnPush,
    PawnDoublePush,
    Castle
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

BoardArray = list[list[(Piece | None)]]
BoardEnumerator = Iterator[tuple[int, int, (Piece | None)]]

class Position:
    """Manages the position logic, such as moves, captures, win/loss, etc."""

    toMove: ColorChar
    castleRights: dict[ColorChar, dict[PieceChar, bool]]
    epTarget: (Coord | None)
    halfMoveClock: int
    fullMoveNumber: int
    fenStr: str
    positionHistory: dict[str, int]   # dictionary of FEN without move counts  

    _board: BoardArray

    def __init__(self, startPos: str = STANDARD_START_POSITION):
        self.fenStr = startPos
        self.setState(startPos)


    def setState(self, fen: str):
        """Sets the game state from a Forsyth-Edwards Notation (FEN) string

        Args:
            fen (str): a FEN string describing the game state
        """
        temp = fen.split(' ')
        self.setPosition(temp[0])
        self.toMove = ColorChar(temp[1])

        self.castleRights = {
            ColorChar.WHITE: {PieceChar.KING: False, PieceChar.QUEEN: False},
            ColorChar.BLACK: {PieceChar.KING: False, PieceChar.QUEEN: False}
        }
        for char in temp[2]:
            if char == 'K':
                self.castleRights[ColorChar.WHITE][PieceChar.KING] = True
            elif char == 'Q':
                self.castleRights[ColorChar.WHITE][PieceChar.QUEEN] = True
            elif char == 'k':
                self.castleRights[ColorChar.BLACK][PieceChar.KING] = True
            elif char == 'q':
                self.castleRights[ColorChar.BLACK][PieceChar.QUEEN] = True

        self.epTarget = FEN.squareToCoord(temp[3]) if temp[3] != '-' else None
        self.halfMoveClock = int(temp[4])
        self.fullMoveNumber = int(temp[5])

        # initial FEN 
        self._updateFEN()

        # set for determining three fold repetition
        self.positionHistory = {}
        self.positionHistory.setdefault( self._getPositionHistoryStr() , 1 )

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
    def numRows(self) -> int:
        """The number of rows the board has"""

        return len(self._board)

    @property
    def numCols(self) -> int:
        """The number of columns the board has"""

        if self.numRows == 0:
            return 0
        return len(self._board[0])

    # define home rows for pawns and home squares for rooks
    def _pawnHomeRow(self, color: ColorChar) -> int:
        return (self.numRows - 2) if color == ColorChar.WHITE else 1

    def _rookHomeSquare(self, color: ColorChar, side: PieceChar) -> Coord:
        row = (self.numRows - 1) if color == ColorChar.WHITE else 0
        col = (self.numCols - 1) if side == PieceChar.KING else 0
        return (row, col)

    def enumerateBoard(self) -> BoardEnumerator:
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

        # next line returns moves before checking if legal
        # return moves

        # check which moves are legal
        return [move for move in moves if not self.moveIntoCheck(move)]

    def _getPiecePseudoLegalMoves(self, row: int, col: int, piece: Piece) -> list[Move]:
        moves = []
        start = (row, col)

        if piece.moveRange == chessPiece.MAX_RANGE:
            moveRange = self.numRows
        else:
            moveRange = piece.moveRange

        if isinstance(piece, Pawn) and row == self._pawnHomeRow(self.toMove):
            moveRange += 1

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
                # move = Move(start,end)
                if isinstance(piece, Pawn) and i == 2:
                    move = PawnDoublePush(start, end)
                else:
                    move = Move(start, end)
                moves.append(move)

        if isinstance(piece, King):
            moves += self._getPiecePseudoLegalCastle(row, col, piece)

        return moves

    def _getPiecePseudoLegalCastle(self, row: int, col: int, piece: Piece) -> list[Move]:
        """Since castling is such a unique move, it will be handled separately here."""

        if not isinstance(piece, King):
            return []

        start = (row, col)
        moves = []
        # Check both kingside and queenside
        for side in [PieceChar.KING, PieceChar.QUEEN]:
            if not self.castleRights[self.toMove][side]:
                continue

            _, rookCol = self._rookHomeSquare(self.toMove, side)

            # check if squares between the king and rook are empty
            startCol = min(col, rookCol) + 1
            endCol = max(col, rookCol)
            if any(piece is not None for piece in self._board[row][startCol:endCol]):
                continue

            moveDir = 1 if side == PieceChar.KING else -1

            # check that the king isn't walking through or into check
            coords = [(row, col + moveDir * (i + 1)) for i in range(2)]
            if any(self.isSquareAttacked(coord, self.toMove.opponent) for coord in coords):
                continue

            newc = col + moveDir * 2
            end = (row, newc)
            moves.append(Castle(start, end))

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

        # Castling
        if isinstance(move, Castle):
            if endCol > startCol:  # Kingside castle
                rookRow, rookCol = self._rookHomeSquare(
                    self.toMove, PieceChar.KING)
                self._board[rookRow][rookCol] = None
                self._board[endRow][endCol-1] = Rook(piece.color)
            else:  # queenside
                rookRow, rookCol = self._rookHomeSquare(
                    self.toMove, PieceChar.QUEEN)
                self._board[rookRow][rookCol] = None
                self._board[endRow][endCol+1] = Rook(piece.color)

        self._updateState(move)
        # print( self.FENstr)

    def _updateState(self, move: Move):

        # Castling rights
        movedPiece = self. _board[move.end[0]][move.end[1]]
        if isinstance(movedPiece, King):
            self.castleRights[self.toMove][PieceChar.KING] = False
            self.castleRights[self.toMove][PieceChar.QUEEN] = False

        elif isinstance(movedPiece, Rook):
            for pieceChar in (PieceChar.KING, PieceChar.QUEEN):
                if move.begin == self._rookHomeSquare(self.toMove, pieceChar):
                    self.castleRights[self.toMove][pieceChar] = False

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
        self.toMove = self.toMove.opponent

        if self.toMove == ColorChar.WHITE:
            self.fullMoveNumber += 1

        self._updateFEN()

        # add the updated position to the positionHistory 
        positionHistoryStr = self._getPositionHistoryStr() 
        self.positionHistory.setdefault( positionHistoryStr, 0 )
        self.positionHistory[ positionHistoryStr ] += 1 

        # print( self.positionHistory ) 

    def _getPositionHistoryStr(self): 
        return ' '.join( self.fenStr.split(' ')[0:4]   ) 


    def _updateFEN(self):
        tempBoardStr = self._getBoardStr()

        # self.castleRights
        castleStr = ''
        if self.castleRights[ColorChar.WHITE][PieceChar.KING]:
            castleStr += 'K'
        if self.castleRights[ColorChar.WHITE][PieceChar.QUEEN]:
            castleStr += 'Q'
        if self.castleRights[ColorChar.BLACK][PieceChar.KING]:
            castleStr += 'k'
        if self.castleRights[ColorChar.BLACK][PieceChar.QUEEN]:
            castleStr += 'q'

        if len(castleStr) == 0:
            castleStr = '-'

        epStr = '-' if not self.epTarget else FEN.coordToSquare(self.epTarget)

        self.fenStr = ' '.join([tempBoardStr, self.toMove.value, castleStr, epStr, str(
            self.halfMoveClock), str(self.fullMoveNumber)])

    def _getBoardStr(self):
        outstr = ''
        for row in range(self.numRows):
            j = 0
            for col in range(self.numCols):
                if self._board[row][col] is None:
                    j += 1
                else:
                    if j != 0:
                        outstr = outstr + \
                            str(j) + str(self._board[row][col])
                    else:
                        outstr = outstr + str(self._board[row][col])
                    j = 0

            if j != 0:
                outstr += str(j)

            outstr += '/'

        return outstr[:-1]    # remove accidentally over included '/'


    def moveToAlgebraic(self, move: Move) -> str: 
        """ BEFORE move is executed, express the algebraic notation of the move. """ 
        # assume that move has not yet been executed
        beginrow, begincol  = move.begin
        endrow, endcol  = move.end
        piece = self._board[beginrow][begincol] 

        # add a + for check. # for checkmate eventually 
        checkStr = '' 
        if self.inCheck( self.toMove ): 
            checkStr = '+'
        # if checkmate... '#' 

        if isinstance( move, Castle): 
            if endcol > begincol: 
                return '0-0' + checkStr  # kingside castle 
            else: 
                return '0-0-0' + checkStr  # queenside castle 

        promoStr = ''
        # if  promotion... (Q)  

        captStr = '' 
        if isinstance( move, Capture ): 
            captStr = 'x'

        if isinstance( piece, Pawn): 
            if isinstance( move, Capture ): 
                headStr = FEN.coordToSquare( move.begin ) [0] 
            else: 
                headStr = '' 
       
        else: 
            headStr = piece.char.value.upper()

            # check no other piece can get to that square. 
            allMoves = self.getLegalMoves(self.toMove )
            for tempMove in allMoves: 
                if (tempMove.end == move.end) and (tempMove.begin != move.begin) and isinstance( self._board[tempMove.begin[0]][tempMove.begin[1]], type(piece) ) : 
                    # Another piece of the same type can move to the end square  

                    if tempMove.begin[0] == move.begin[0]: 
                        headStr += FEN.coordToSquare(move.begin)[0]   # get letter of beginning square 
                    else: 
                        headStr += FEN.coordToSquare(move.begin)[1]   # get number of beginning square 

        return headStr + captStr + FEN.coordToSquare(move.end) + promoStr + checkStr 


    def findKing(self, color: ColorChar) -> Coord:
        """Returns the position of the king of the given color"""

        for row, col, piece in self.enumerateBoard():
            if isinstance(piece, King) and piece.color == color:
                return (row, col)

        raise Exception(f"No {color} king found!")

    def inCheck(self, color: ColorChar) -> bool:
        """Returns whether the player of the given color is in check"""

        kingPos = self.findKing(color)
        return self.isSquareAttacked(kingPos, color.opponent)

    def moveIntoCheck(self, move: Move) -> bool:
        """Returns whether the given move would put the player toMove in check."""

        tempPosition = Position(self.fenStr)
        tempPosition.executeMove(move)

        return tempPosition.inCheck(self.toMove)

    def countPiece(self, pieceToFind: type[Piece]) -> dict[ColorChar, int]:
        """Find the number of piece of each color on the board"""

        countDict = {ColorChar.WHITE: 0, ColorChar.BLACK: 0}
        for _, _, piece in self.enumerateBoard():
            if isinstance(piece, pieceToFind):
                countDict[piece.color] += 1
        return countDict

    def illegalPawnPlacement(self) -> bool:
        """ detects if pawns are in invalid positions. (1st or last rank) """
        for row in (0, self.numRows-1):
            for piece in self._board[row]:
                if isinstance(piece, Pawn):
                    return True

        return False

    def getPositionStatus(self) -> PositionStatus:
        """ returns a string the reports the status of a position and message describing """

       
        # check if position is valid based on number of kings and if a check had been missed and if pawns aren't in valid position
        kingCount = self.countPiece( King ) 
        if (kingCount[ColorChar.WHITE]!= 1) or (kingCount[ColorChar.BLACK]!= 1) or self.inCheck( self.toMove.opponent ) or self.illegalPawnPlacement(): 
            # return 'invalid' 
            return PositionStatus.INVALID 

        elif self.halfMoveClock == 100: 
            # return 'draw 50 Move Rule' 
            return PositionStatus.FIFTY_MOVE_DRAW

        # elif value of FEN dictionary is 3 : return 'draw 3 fold repetition'   

        elif len( self.getLegalMoves( self.toMove ) ) == 0: 
            if self.inCheck( self.toMove ) and self.toMove == ColorChar.WHITE: 
                return PositionStauts.WHITE_WINS 
            elif self.inCheck( self.toMove ) and self.toMove == ColorChar.BLACK: 
                return PositionStauts.BLACK_WINS
                #return 'checkmate' 
            else: 
                # return 'stalemate' 
                return PositionStatus.STALEMATE 

        if any( value > 2 for value in self.positionHistory.values() ) : 
            return PositionStatus.THREEFOLD_DRAW

        # if the material is not enough to mate 
        material = self.materialCount() 
        pawnCount = self.countPiece(Pawn) 
        if not any( val > 0 for val in  pawnCount.values() ) and material[ColorChar.WHITE] + material[ColorChar.BLACK] < 4: 
            return PositionStatus.INSUFFICIENT_DRAW  # for now ignore insufficient draw of K + B vs K + B if bishop on same color squares 

        return PositionStatus.IN_PLAY



    # # Functions used to evaluate the position -------------------------------- 
    def materialCount(self ) -> dict[ColorChar, int]: 
        """Counts the relative value of material on the board for white and black""" 
        material = {ColorChar.WHITE: 0, ColorChar.BLACK: 0} 
        for _, _, piece in self.enumerateBoard():
            if piece and not isinstance(piece,King):
                material[piece.color] += piece.value

        return material 


    # def findCheckmate(self) -> 





