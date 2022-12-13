#!/bin/python

# 2022.07.26
# fen.py

from typedefs import Coord


def squareToCoord(square: str) -> Coord:
    """Converts a square location a1 etc. to the corresponding (row, col) tuple"""
    rowDict = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    colDict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    if len(square) != 2 or square[0] not in colDict or square[1] not in rowDict:
        raise ValueError(f'Invalid Coordinate in function coorToNum: {square}')

    return (rowDict[square[1]], colDict[square[0]])


def coordToSquare(coord: Coord) -> str:
    """Converts a (row, col) tuple to the corresponding square location"""
    rowDict = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    colDict = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    if coord[0] not in rowDict or coord[1] not in colDict:
        raise ValueError('Invalid row,col array in function numToCoor')

    return colDict[coord[1]] + rowDict[coord[0]]


# class FEN:
#     def getBoardStr(self):

#         outstr = ''
#         for r in range(self.nrows):
#             j = 0
#             for c in range(self.nrows):
#                 if self._board[r][c] == None:
#                     j += 1

#                 else:
#                     outstr = outstr + str(j) + str(self._board[r][c])
#                     j = 0

#             if j != 0:
#                 outstr += str(j)

#             outstr += '/'

#         return outstr[:-1]  # remove accidentally over included '/'

#     def updateFEN(self, move):
#         '''
#         update the FEN after a move
#           move -- a move object or subclass of move object, the flags are within the move motion
#           eventually include a flags argument for special moves
#         '''

#         tempBoardStr = self.getBoardStr()

#         # ep rights
#         if isinstance(move, chessMove.PawnTwoSquare):
#             r, c = gf.coorToNum(move.end)
#             if self.toMove == 'w':  # white is making the pawn move
#                 self.epTarget = gf.numToCoor([r+1, c])
#             else:  # black made the pawn move
#                 self.epTarget = gf.numToCoor([r-1, c])

#         else:
#             self.epTarget = '-'   # ep only applies for the first available move

#         self.FEN = ' '.join([tempBoardStr, self.toMove, self.castleRights, self.epTarget, str(
#             self.halfMoveClock), str(self.fullMoveNumber)])
