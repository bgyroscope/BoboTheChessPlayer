#!/bin/python

# 2022.07.26
# fen.py

from typedefs import Point


def coordToNum(loc: str) -> Point:
    ''' convert square location a1 etc. to numbers in array 7,0 '''
    rowdict = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    coldict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    if len(loc) != 2 or loc[0] not in coldict or loc[1] not in rowdict:
        raise ValueError(f'Invalid Coordinate in function coorToNum: {loc}')

    return (rowdict[loc[1]], coldict[loc[0]])


def numToCoord(rowcol):
    ''' converts [r,c] array to square location '''
    rowdict = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    coldict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    if len(rowcol) != 2 or rowcol[0] not in rowdict or rowcol[1] not in coldict:
        raise ValueError('Invalid row,col array in function numToCoor')

    return coldict[rowcol[1]] + rowdict[rowcol[0]]


class FEN:
    def getBoardStr(self):

        outstr = ''
        for r in range(self.nrows):
            j = 0
            for c in range(self.nrows):
                if self._board[r][c] == None:
                    j += 1

                else:
                    outstr = outstr + str(j) + str(self._board[r][c])
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

        # ep rights
        if isinstance(move, chessMove.PawnTwoSquare):
            r, c = gf.coorToNum(move.end)
            if self.toMove == 'w':  # white is making the pawn move
                self.epTarget = gf.numToCoor([r+1, c])
            else:  # black made the pawn move
                self.epTarget = gf.numToCoor([r-1, c])

        else:
            self.epTarget = '-'   # ep only applies for the first available move

        self.FEN = ' '.join([tempBoardStr, self.toMove, self.castleRights, self.epTarget, str(
            self.halfMoveClock), str(self.fullMoveNumber)])
