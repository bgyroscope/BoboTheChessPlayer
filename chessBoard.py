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



    def checkStatus(self, color, moveArr=None): 
        ''' check the status of the game ---> for now use number of kings or valid moves as a proxy
            color = 'w' or 'b' 
            moveArr is the result from possibleMoves. None by default to indicate that we must call possibleMoves   
                returns "in prog", "invalid", "draw", "checkmate" 
        ''' 

        # find the kings 
        nw, nb = self.findKings()
        if nw == 0 and  nb == 0 or nw > 1 or nb > 1:
            return "invalid" 

        if nw == 1 and nb == 1: 

            if not moveArr: 
                moveArr = self.possibleMoves( color ) 

            if moveArr == []: 
                return "draw" 
            else: return "in prog" 

        else: 
            if (color == 'w' and nw == 0 ) or ( color == 'b' and nb == 0 ):  
                return "checkmate"  
            else: 
                return "invalid"


    def findKings( self) : 
        ''' returns number of white then number of black kings ''' 
        nw = 0 
        nb = 0 

        for row in self.arr: 
            for p in row: 
                if isinstance( p, cp.King ) : 
                    if p.color == 'w' : nw += 1
                    else: nb += 1 

        return [nw,nb] 




    def possibleMoves(self, color ): 
        ''' find the valid moves on the board for pieces of given color
            color = 'w' or 'b' (color of the person to move. (Probably should be board.toMove)  
            Return an array of possible moves -- move objects ''' 

        moveArr = [] 

        for r, row  in enumerate(self.arr): 
            for c, p in enumerate(row): 
                if p != None and p.color == color: 
                    # look for valid moves
                    begin = gf.numToCoor( [r,c] ) 

                    # ----------------------------------------------
                    # pawns are funky. Special instructions for them 
                    # ----------------------------------------------
                    if isinstance( p, cp.Pawn ):
                       
                        # initial move 
                        if ( color == 'w' and r == 6) or (color == 'b' and r==1): 
                            tempMaxRange = 2 
                        else: 
                            tempMaxRange = 1 

                        # forward motion-------------------- 
                        for j in range(1,tempMaxRange+1): 
                            newr, newc = r + p.direction[0][0]*j , c + p.direction[0][1] * j    # p.direction = [ [delr , delc] ]  

                            if newr<0 or newr >= self.nrows or newc < 0 or newc >= self.nrows: 
                                break 

                            end = gf.numToCoor( [ newr, newc  ]  ) 

                            # promotion  --- condition of making it to the last rank 

                            if self.arr[ newr ][ newc ]   == None: 
                                if j == 1: 
                                    moveArr.append(  cm.PawnOneSquare( begin, end )  ) 
                                else: 
                                    moveArr.append(  cm.PawnTwoSquare( begin, end )  ) 

                            else:
                                # cannot move forward to square already occupied by a piece 
                                break  

                        # capture and ep    -------------------------- 
                        for direc in p.capDirection:
                            # here the loop is over the direction (not range) thus continue rather than break 
                            newr, newc = r + direc[0], c + direc[1] 
                            if newr<0 or newr >= self.nrows or newc < 0 or newc >= self.nrows: 
                                continue

                            end = gf.numToCoor( [ newr, newc  ]  )

                            if self.arr[newr][newc] != None and self.arr[newr][newc].color != color :
                                moveArr.append( cm.Capture( begin, end )  )
                                continue 
                               
                            # check for ep here 
                            elif [newr, newc] == gf.coorToNum( self.epRights ): 
                                moveArr.append( cm.PawnEP(begin, end) )
                                continue

                            else:
                                # can only move diagonal if there is a capture 
                                continue 


                    # ----------------------------------------------
                    #  All other pieces 
                    # ----------------------------------------------
 
                    else: 
                        # for all the other pieces ... 
                        for direc in p.direction: 
                            for j in range(1,p.maxRange+1):
                                # continue to add valid moves until it encounters another piece. 
                                newr, newc = r+direc[0]*j ,  c + direc[1] * j 

                                if newr<0 or newr >= self.nrows or newc < 0 or newc >= self.nrows: 
                                    break 

                                end = gf.numToCoor( [ newr, newc  ]  ) 

                                if self.arr[ newr ][ newc ]   == None: 
                                    moveArr.append(  cm.Simple( begin, end )  ) 

                                elif self.arr[newr][newc].color != color :
                                    moveArr.append( cm.Capture( begin, end )  )
                                    break 
                                    
                                else:
                                    # cannot move to square with own piece 
                                    break  

        # now also consider the special moves like ep and castling 
        # also must check if a move puts the player in check 

        return moveArr 


    def executeMove(self, move ): 
        ''' make a move on the board
            move -- instance of class Move 
        ''' 
        
        b = gf.coorToNum( move.begin ) 
        e = gf.coorToNum( move.end   ) 

        self.arr[e[0] ][ e[1] ] = self.arr[b[0] ][ b[1] ]
        self.arr[b[0] ][ b[1] ] = None
        
        # other conditions
        if isinstance( move, cm.PawnEP): 
            # have to remove the captured pawn, whose location depends on color 
            if self.toMove == 'w': 
                self.arr[ e[0]+1 ][ e[1] ] = None 
            else: # b
                self.arr[ e[0]-1 ][ e[1] ] = None 
                

        # update the FEN and other variables 
        # eventually include flags for updating ep, castling, and halfMoveClock
        self.updateFEN( move ) 


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



    def updateFEN(self, move ): 
        ''' update the FEN after a move  
            move -- a move object or subclass of move object, the flags are within the move motion 
            eventually include a flags argument for special moves 
        ''' 
 
        tempBoardStr = self.getBoardStr() 
       
        # changes due to flags 
        # self.castleRights = ? 
        # self.epRights = ? 


        # ep rights
        if isinstance( move, cm.PawnTwoSquare ): 
            r,c = gf.coorToNum( move.end )
            if self.toMove == 'w':  # white is making the pawn move 
                self.epRights = gf.numToCoor( [r+1,c] ) 
            else: # black made the pawn move 
                self.epRights = gf.numToCoor( [r-1,c] ) 

        else: 
            self.epRights = '-'   # ep only applies for the first available move 

        # half move clock can be reset by pawn moves or capture.
        if isinstance( move, cm.PawnMove ) or isinstance(move, cm.Capture):  
            self.halfMoveClock = 0 
        else: 
            self.halfMoveClock += 1 


        # update whose move it is at the end 
        if self.toMove == 'w': 
            self.toMove = 'b'
       
        else: 
            self.toMove = 'w' 
            self.fullMoveNumber += 1 


        self.FEN = ' '.join( [tempBoardStr, self.toMove, self.castleRights, self.epRights, str( self.halfMoveClock) , str( self.fullMoveNumber) ]  ) 



    # Other class methods ---------------------------------------------------------------------------
    @classmethod
    def createEmptyBoard(cls): 
        return cls( "8/8/8/8/8/8/8/8 w - - 0 1" )










