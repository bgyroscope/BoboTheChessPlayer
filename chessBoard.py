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


import genFun     as gf 
import chessPiece as cp 
import chessMove  as cm

class Board: 
    nrows = 8 

    def __init__(self, FEN="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w kqKQ - 0 1"): 
        ''' 
        FEN is a string Forsyth-Edwards Notation 
            eventually     pos -- set of all FEN taht have been reached before (for three fold repetition) 
        '''

        self.FEN = FEN
        self.pos = set();   # set for determining three fold repetition  
        self.arr = []       # stores the pieces on the board  

        # self.toMove, self.castleRights, self.epRights, self.halfMoveClock, self.fullMoveNumber = 
        self.interpretFEN()
        # set up the pieces and the charArr 
        self.setUpBoard() 

    def __repr__(self): 
        return  self.FEN


    def __str__(self):
        return self.FEN

    def display(self): 
        print( ) 
        for i, row in enumerate( self.arr ):  
            print( "  " + "-" * 32  ) 
            print( str(8-i) + " ", end = "| " ) 
            for elm in row: 
                if elm: 
                    print( elm, end=" | " ) 
                else: 
                    print( " ", end=" | " ) 
            print() 

        print( "  " + "-" * 32  ) 
        print( '    ' + '   '.join([ c for c in 'abcdefgh'] )   ) 
        print( ) 
        print( self.toMove + ' to move\n' ) 



    # Initial set up from FEN -----------------------------------------------------------
    def setUpBoard (self): 
        ''' Get the array of the board from the FEN ''' 

        digstr = '12345678' 
        
        boardstr = self.FEN.split(" ") [0] 
        temp = boardstr.split("/") 

        self.arr = [ [ None  for j in range(self.nrows) ] for j in range(self.nrows) ]

        for r,row in enumerate(temp): 
            c = 0
            for char in row: 
                if char in digstr: 
                    c += int(char) 
                else: 
                    # found a piece in input str 
                    self.arr[r][c] = cp.createPiece( char  ) 

                    c += 1 


    def interpretFEN(self): 
        '''method to interpret FEN '''
        temp = self.FEN.split(" ") 
        self.toMove, self.castleRights, self.epRights = temp[1:4] 
        self.halfMoveClock = int( temp[4] ) 
        self.fullMoveNumber  = int( temp[5] ) 



    # Making moves on the board -------------------------------------------------------------------------
    


    # def isSquareEmpty(self, loc): 
    #     ''' return bool if the square is unoccupied ''' 

    #     return True 


    # def isSquareAttacked(self,loc, color): 
    #     ''' returns bool if the square is attacked by color piece ''' 



    def possibleMoves(self, color ): 
        ''' find the valid moves on the board for pieces of given color
            color = 'w' or 'b' 
            Return an array of possible moves -- move objects ''' 

        moveArr = [] 

        for r, row  in enumerate(self.arr): 
            for c, p in enumerate(row): 
                if p != None and p.color == color: 
                    # look for valid moves
                    begin = gf.numToCoor( [r,c] ) 

                    for direc in p.direction: 
                        for j in range(1,p.maxRange+1):
                            # continue to add valid moves until it encounters another piece. 
                            x, y = r+direc[0]*j ,  c + direc[1] * j 

                            if x<0 or x >= self.nrows or y < 0 or y >= self.nrows: 
                                break 

                            end = gf.numToCoor( [ x, y  ]  ) 

                            if self.arr[ x ][ y ]   == None: 
                                moveArr.append(  cm.Simple( begin, end )  ) 

                            elif self.arr[x][y].color != color :
                                moveArr.append( cm.Capture( begin, end )  )
                                break 
                                
                            else:
                                # cannot move to square with own piece 
                                break  

        # now also consider the special moves like ep and castling 

        return moveArr 


    def executeMove(self, move ): 
        ''' make a move on the board
            move -- instance of class Move 
        ''' 
        
        b = gf.coorToNum( move.begin ) 
        e = gf.coorToNum( move.end   ) 

        self.arr[e[0] ][ e[1] ] = self.arr[b[0] ][ b[1] ]
        self.arr[b[0] ][ b[1] ] = None
        
        # other conditions....

        # update the FEN and other variables 
        # eventually include flags for updating ep, castling, and halfMoveClock
        self.updateFEN() 


    # # # Output FEN from board ------------------------------------------------------------------------
    def getBoardStr(self):

        outstr = '' 
        for r in range(self.nrows): 
            j = 0 
            for c in range(self.nrows): 
                if self.arr[r][c] == None: 
                    j += 1 

                else: 
                    outstr = outstr +  str(j)  + self.arr[r][c].__str__() 
                    j = 0 

            if j != 0 : 
                outstr += str(j) 

            outstr += '/' 

        return outstr[:-1]    # remove accidentally over included '/'  



    def updateFEN(self ): 
        ''' update the FEN after a move  
            eventually include a flags argument for special moves 
        ''' 
 
        tempBoardStr = self.getBoardStr() 

        if self.toMove == 'w': 
            self.toMove = 'b'
       
        else: 
            self.toMove = 'w' 
            self.fullMoveNumber += 1 

       
        # changes due to flags 
        # self.castleRights = ? 
        # self.epRights = ? 


        # half move clock can be reset by pawn moves or capture. 
        # for now just increment it 
        self.halfMoveClock += 1 


        self.FEN = ' '.join( [tempBoardStr, self.toMove, self.castleRights, self.epRights, str( self.halfMoveClock) , str( self.fullMoveNumber) ]  ) 



    # Other class methods ---------------------------------------------------------------------------
    @classmethod
    def createEmptyBoard(cls): 
        return cls( "8/8/8/8/8/8/8/8 w - - 0 1" )










