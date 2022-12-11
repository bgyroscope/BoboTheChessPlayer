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

        # dictionary for converting from string rep to unicode 
        helpdict ={ 'K': '\u2654',  'Q': '\u2655', 'R': '\u2656', 'B': '\u2657', 'N': '\u2658', 'P': '\u2659',
                    'k': '\u265A',  'q': '\u265B', 'r': '\u265C', 'b': '\u265D', 'n': '\u265E', 'p': '\u265F'
        }  

        print( ) 
        for i, row in enumerate( self.arr ):  
            print( "  " + "-" * 32  ) 
            print( str(8-i) + " ", end = "| " ) 
            for elm in row: 
                if elm: 
                    # print( elm, end=" | " ) 
                    print( helpdict[str(elm)], end=" | " ) 
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
    def checkStatus(self, color, moveArr=[] ): 
        ''' check the status of the game ---> for now use number of kings or valid moves as a proxy
            color = 'w' or 'b' 
            moveArr is the result from validMoves. empty array by default to indicate that we must call validMoves   
                returns "in prog", "invalid", "draw", "checkmate" 
        ''' 

        # find the kings 
        # nw, nb = self.findKings()
        wkloc, bkloc = self.findKings()
        nw, nb = len(wkloc), len(bkloc) 

        if nw == 0 and  nb == 0 or nw > 1 or nb > 1:
            return "invalid" 

        if nw == 1 and nb == 1: 

            if not moveArr: 
                # moveArr = self.possibleMoves( color ) 
                moveArr = self.validMoves( color ) 

            if moveArr == []: 
                return "draw" 
            else: return "in prog" 

        else: 
            if (color == 'w' and nw == 0 ) or ( color == 'b' and nb == 0 ):  
                return "checkmate"  
            else: 
                return "invalid"


    def findKings( self) : 
        ''' returns locations of white then number of black kings ''' 
        wkloc = []  # white king location 
        bkloc = [] 

        for r, row in enumerate( self.arr ): 
            for c, p in enumerate(row): 
                if isinstance( p, cp.King ) : 
                    # if p.color == 'w' : nw += 1
                    # else: nb += 1 
                    if p.color == 'w' : wkloc += [gf.numToCoor([r,c]) ]
                    else: bkloc += [gf.numToCoor([r,c]) ]  

        # return [nw,nb] 
        return [wkloc,bkloc] 



    def inCheck(self, color, moveArr=[]):
        ''' function determines if player of color 'color' is in check. 
        color = 'w' or 'b'. 
        moveArr is the possible moves. If None, then possible moves is called. 
        Return True or False. '''
        # get the king location.
        wkloc, bkloc = self.findKings()
        if color == 'w': 
            kingloc = wkloc[0];  
            # otherColor = 'b'
        else: 
            kingloc = bkloc[0];  
            # otherColor = 'w'
        

        # if not moveArr: 
        #     moveArr = self.possibleMoves( otherColor )


        for move in moveArr: 
            if move.end == kingloc: 
                return True 


        return False 



    def validMoves(self, color, moveArr=[]): 
        ''' determines all valid moves on the board for pieces of a given color, handling isues of check. 
        color = 'w' or 'b' (color of player to move)
        Return an array of valid moves (move objects) ''' 

        if not moveArr: 
            moveArr = self.possibleMoves(color) 


        if color == 'w': otherColor = 'b'
        else: otherColor = 'w' 


        validMoveArr = [] 

        for move in moveArr: 

            # print( self.FEN) 

            # check if King is in check after the move.
            tempBoard = Board( self.FEN ) 
            tempBoard.executeMove( move )
            tempMoveArr = tempBoard.possibleMoves( tempBoard.toMove ) 

            # print( move) 
            # self.display()  
            # tempBoard.display() 
            # print( 'Is ', color, ' in check?', tempBoard.inCheck(color) ) 

            if not tempBoard.inCheck( color, tempMoveArr  ):  
                validMoveArr.append(move)  


        return validMoveArr 


    ## finds all the possible moves for a player ignoring check issues.  
    def possibleMoves(self, color ): 
        ''' find the valid moves on the board for pieces of given color. 
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

                            if self.arr[ newr ][ newc ]   == None: 
                                if j == 1 and (newr==0 or newr==7 ): 
                                    # promotion -- (assuming pawns don't move backwards, ie white pawn can't get to newr==7) 
                                    for flag in [ 'Q', 'R', 'B', 'N' ] : 
                                        moveArr.append(  cm.PawnPromote( begin, end, flag )  ) 

                                elif j == 1: 
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
                            elif self.epRights != '-' and [newr, newc] == gf.coorToNum( self.epRights ): 
                                moveArr.append( cm.PawnEP(begin, end) )
                                continue

                            else:
                                # can only move diagonal if there is a capture 
                                continue 


                    # ----------------------------------------------
                    #  All other pieces 
                    # ----------------------------------------------
 
                    else: 

                        # check if castling is possible for king. -----------------------------------------------------------------
                        if isinstance( p, cp.King ):  
                            
                            helpdir = { 'k': 1, 'q': -1 }  # for specifying direction  

                            # check FEN flags 
                            if color == 'w': testFlags = 'KQ'
                            else: testFlags = 'kq'

                            for flag in testFlags: 
                                if flag in self.castleRights:
                                    # direction relies on the FEN flag being correct
                                    newr, newc = r, c + 2*helpdir[flag.lower()] 
                                    # if newr<0 or newr >= self.nrows or newc < 0 or newc >= self.nrows: 
                                    #     continue 
                                    end = gf.numToCoor( [ newr, newc ] ) 

                                    # check that the spaces are empty between king and rook  
                                    lastj = 3 + (1 - helpdir[flag.lower()] ) // 2   # queenside has 3 spaces to check while kingside has only 2 spaces. 
                                                                                    # lastj is 3 + ( 1 - (-1) )//2 = 4 for queenside vs 3  for kingside 

                                    if sum( [ self.arr[r][c+helpdir[flag.lower()]*j] == None for j in range(1,lastj) ] ) == lastj - 1 :

                                        # check it doesn't move through check (lands in check is tested by valid move)  
                                        tempBoard = Board( self.FEN )
                                        move = cm.Simple( gf.numToCoor([r,c]) , gf.numToCoor([r, c+ helpdir[flag.lower()] ] ) )
                                        tempBoard.executeMove( move )
                                        tempMoveArr = tempBoard.possibleMoves( tempBoard.toMove ) 
                                        if not tempBoard.inCheck( color, tempMoveArr ): 
                                            moveArr.append( cm.Castle(begin, end, flag) ) 
 


                        # for all the other simple moves -----------------------------------------------------------------
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

        elif isinstance( move, cm.PawnPromote): 
            # promotion depends on whose move it is
            if self.toMove == 'w': 
                char = move.promoteFlag.upper() 
            else: # black 
                char = move.promoteFlag.lower() 

            self.arr[e[0] ][ e[1] ] = cp.createPiece( char  )  


        # castling -- have to move the rook, too 
        elif isinstance( move, cm.Castle ): 
            if move.castleFlag.lower() == 'k': 
                self.arr[b[0] ][ e[1]-1 ]  = self.arr[b[0] ][ 7 ] 
                self.arr[b[0] ][ 7 ] = None 
            elif move.castleFlag.lower() == 'q': 
                self.arr[b[0] ][ e[1]+1 ]  = self.arr[b[0] ][ 0 ] 
                self.arr[b[0] ][ 0 ] = None 


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
                    if j!=0: 
                        outstr = outstr +  str(j)  + self.arr[r][c].__str__() 
                    else: 
                        outstr = outstr + self.arr[r][c].__str__() 

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
        # castling rights -- if castle change self.castleRights = '-'. Also must check for king or rook move (based on c)  
        r,c = gf.coorToNum( move.end ) 
        movedPiece = self.arr[r][c]
        # no more castling rights if the piece that moved (or castle but that should already be covered by king moved)  #  or isinstance( move, cm.Castle):
        if isinstance( movedPiece, cp.King) or isinstance(movedPiece, cp.Rook):
            if isinstance( movedPiece, cp.King ): 
                toRemove = 'kq'
            else:
                rbegin, cbegin = gf.coorToNum( move.begin) 
                if cbegin == 0: 
                    toRemove = 'q'
                elif cbegin == 7: 
                    toRemove = 'k' 

            if self.toMove == 'w': toRemove = toRemove.upper()   # make uppercase for white pieces  

            newCastleRights = '' 
            for char in self.castleRights: 
                if char not in toRemove: 
                    newCastleRights += char 

            self.castleRights = newCastleRights



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


        # update whose move it is at the end ----------------------------
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










