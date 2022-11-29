#!/bin/python

# 2022.07.26
# chessboard.py -- defines the Board object
# Properties:
#   FEN -- the Forsyth-Edwards Notation of the current position
#   pos -- a set of all the FEN (minus castle rights, ep rights, half move clock and full move number) for three fold repetition
#   arr -- board array None if empty, else a piece


# Methods:
#   init -- initialize from an FEN (default vaue is initial position)
#   repr -- return FEN
#   str --  same as rerpr
#   display -- prints out the charArr of the board

import pygame

import genFun as gf
import chessPiece as cp
import chessMove as cm


class Board:
    ncols = nrows = 8

    def __init__(self, FEN):
        self.pos = set()  # set for determining three fold repetition
        self.arr = []     # stores the pieces on the board

        self.parseFEN(FEN)

    def __repr__(self):
        return self.FEN

    def __str__(self):
        return self.FEN

    def parseFEN(self, FEN):
        temp = FEN.split(' ')
        self.setPosition(temp[0])
        self.toMove, self.castleRights, self.epTarget = temp[1:4]
        self.halfMoveClock = int(temp[4])
        self.fullMoveNumber = int(temp[5])

    def render(self):
        board = pygame.image.load('images/chess_board.png').convert()
        for r, row in enumerate(self.arr):
            for c, elm in enumerate(row):
                if elm is not None:
                    piece = elm.render()
                    board.blit(piece, (c * 100, r * 100))
        return board

    # Initial set up from FEN -----------------------------------------------------------

    def setPosition(self, boardstr):
        '''
        boardstr - the board position in Forsyth-Edwards Notation
        eptarget - the current en passant target
        '''
        temp = boardstr.split("/")

        self.arr = [[None] * self.ncols for _ in range(self.nrows)]

        for r, row in enumerate(temp):
            c = 0
            for char in row:
                if char in '12345678':
                    c += int(char)
                else:
                    # found a piece in input str
                    self.arr[r][c] = cp.createPiece(char)
                    c += 1

    def getPieceAt(self, row, col):
        return self.arr[row][col]

    # Making moves on the board -------------------------------------------------------------------------

    # def isSquareEmpty(self, loc):
    #   ''' return bool if the square is unoccupied '''

    #   return True

    # def isSquareAttacked(self,loc, color):
    #   ''' returns bool if the square is attacked by color piece '''

    def checkStatus(self, color, moveArr=None):
        ''' check the status of the game ---> for now use number of kings or valid moves as a proxy
          color = 'w' or 'b' 
          moveArr is the result from possibleMoves. None by default to indicate that we must call possibleMoves   
            returns "in prog", "invalid", "draw", "checkmate" 
        '''

        # find the kings
        nw, nb = self.findKings()
        if nw == 0 and nb == 0 or nw > 1 or nb > 1:
            return "invalid"

        if nw == 1 and nb == 1:

            if not moveArr:
                moveArr = self.possibleMoves(color)

            if moveArr == []:
                return "draw"
            else:
                return "in prog"

        else:
            if (color == 'w' and nw == 0) or (color == 'b' and nb == 0):
                return "checkmate"
            else:
                return "invalid"

    def findKings(self):
        ''' returns number of white then number of black kings '''
        nw = 0
        nb = 0

        for row in self.arr:
            for p in row:
                if isinstance(p, cp.King):
                    if p.color == 'w':
                        nw += 1
                    else:
                        nb += 1

        return (nw, nb)

    def possibleMoves(self, row, col):
        '''
        returns a list of valid moves on the board for the piece at (row, col)
        '''
        def coordOutOfBounds(row, col):
            return newr < 0 or newr >= self.nrows or newc < 0 or newc >= self.ncols

        moves = []

        piece = self.arr[row][col]
        if piece is None:
            return moves

        begin = gf.numToCoor([row, col])

        # ----------------------------------------------
        # Pawns are funky. Special instructions for them
        # ----------------------------------------------
        if isinstance(piece, cp.Pawn):
            # initial move
            if (piece.color == 'w' and row == 6) or (piece.color == 'b' and row == 1):
                tempMaxRange = 2
            else:
                tempMaxRange = 1

            # forward motion--------------------
            for i in range(1, tempMaxRange + 1):
                # p.direction = [ [delr , delc] ]
                newr = row + piece.direction[0][0] * i
                newc = col + piece.direction[0][1] * i

                if coordOutOfBounds(newr, newc):
                    break

                end = gf.numToCoor([newr, newc])

                if self.arr[newr][newc] is None:
                    if i == 1 and (newr == 0 or newr == 7):
                        # promotion -- (assuming pawns don't move backwards, ie white pawn can't get to newr==7)
                        for flag in ['Q', 'R', 'B', 'N']:
                            moves.append(cm.PawnPromote(begin, end, flag))
                    elif i == 1:
                        moves.append(cm.PawnOneSquare(begin, end))
                    else:
                        moves.append(cm.PawnTwoSquare(begin, end))
                else:
                    # cannot move forward to square already occupied by a piece
                    break

            # capture and ep  --------------------------
            for direc in piece.capDirection:
                newr = row + direc[0]
                newc = col + direc[1]

                # here the loop is over the direction (not range) thus continue rather than break
                if coordOutOfBounds(newr, newc):
                    continue

                end = gf.numToCoor([newr, newc])

                if self.arr[newr][newc] is not None and self.arr[newr][newc].color != piece.color:
                    moves.append(cm.Capture(begin, end))
                # check for ep here
                elif self.epTarget != '-' and (newr, newc) == gf.coorToNum(self.epTarget):
                    moves.append(cm.PawnEP(begin, end))

        # ----------------------------------------------
        #  All other pieces
        # ----------------------------------------------
        else:
            # for all the other pieces ...
            for direc in piece.direction:
                for i in range(1, piece.maxRange + 1):
                    # continue to add valid moves until it encounters another piece.
                    newr = row + direc[0] * i
                    newc = col + direc[1] * i

                    if coordOutOfBounds(newr, newc):
                        break

                    end = gf.numToCoor([newr, newc])

                    if self.arr[newr][newc] is None:
                        moves.append(cm.Simple(begin, end))
                    elif self.arr[newr][newc].color != piece.color:
                        moves.append(cm.Capture(begin, end))
                        break
                    else:
                        # cannot move to square with own piece
                        break

        # now also consider the special moves like ep and castling
        # also must check if a move puts the player in check

        return moves

    def executeMove(self, move):
        '''
        make a move on the board
          move -- instance of class Move 
        '''

        b = gf.coorToNum(move.begin)
        e = gf.coorToNum(move.end)

        self.arr[e[0]][e[1]] = self.arr[b[0]][b[1]]
        self.arr[b[0]][b[1]] = None

        # other conditions
        if isinstance(move, cm.PawnEP):
            # have to remove the captured pawn, whose location depends on color
            if self.toMove == 'w':
                self.arr[e[0]+1][e[1]] = None
            else:  # b
                self.arr[e[0]-1][e[1]] = None

        elif isinstance(move, cm.PawnPromote):
            # promotion depends on whose move it is
            if self.toMove == 'w':
                char = move.promoteFlag.upper()
            else:  # black
                char = move.promoteFlag.lower()

            self.arr[e[0]][e[1]] = cp.createPiece(char)

        # update the FEN and other variables
        # eventually include flags for updating ep, castling, and halfMoveClock
        self.updateFEN(move)

    # # # Output FEN from board ------------------------------------------------------------------------

    def getBoardStr(self):

        outstr = ''
        for r in range(self.nrows):
            j = 0
            for c in range(self.nrows):
                if self.arr[r][c] == None:
                    j += 1

                else:
                    outstr = outstr + str(j) + self.arr[r][c].__str__()
                    j = 0

            if j != 0:
                outstr += str(j)

            outstr += '/'

        return outstr[:-1]  # remove accidentally over included '/'

    def updateFEN(self, move):
        '''
        update the FEN after a move  
          move -- a move object or subclass of move object, the flags are within the move motion 
          eventually include a flags argument for special moves 
        '''

        tempBoardStr = self.getBoardStr()

        # changes due to flags
        # self.castleRights = ?
        # self.epTarget = ?

        # ep rights
        if isinstance(move, cm.PawnTwoSquare):
            r, c = gf.coorToNum(move.end)
            if self.toMove == 'w':  # white is making the pawn move
                self.epTarget = gf.numToCoor([r+1, c])
            else:  # black made the pawn move
                self.epTarget = gf.numToCoor([r-1, c])

        else:
            self.epTarget = '-'   # ep only applies for the first available move

        # half move clock can be reset by pawn moves or capture.
        if isinstance(move, cm.PawnMove) or isinstance(move, cm.Capture):
            self.halfMoveClock = 0
        else:
            self.halfMoveClock += 1

        # update whose move it is at the end
        if self.toMove == 'w':
            self.toMove = 'b'
        else:
            self.toMove = 'w'
            self.fullMoveNumber += 1

        self.FEN = ' '.join([tempBoardStr, self.toMove, self.castleRights, self.epTarget, str(
            self.halfMoveClock), str(self.fullMoveNumber)])

    # Other class methods ---------------------------------------------------------------------------

    @classmethod
    def createEmptyBoard(cls):
        return cls("8/8/8/8/8/8/8/8 w - - 0 1")
