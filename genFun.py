#!/bin/python

# 2022.07.26 
# genFun.py -- general functions that will be useful 


colordict = { 'w': 'white', 'b': 'black' } 

def coorToNum( loc ): 
    ''' convert square location a1 etc  to numbers in array  7,0 ''' 
    rowdict = { '1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0 };   
    coldict = { 'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7 }; 

    if len(loc) != 2 or loc[0] not in coldict or loc[1] not in rowdict: 
        print( 'Invalid Coordinate in function coorToNum ' ) 
        return [] 

    else: 
        return [ rowdict[ loc[1] ], coldict[loc[0] ]  ]


def numToCoor( rowcol ): 
    ''' converts [r,c] array to square location '''
    rowdict = { 0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1' };   
    coldict = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }; 

    if len(rowcol) !=2 or rowcol[0] not in rowdict or rowcol[1] not in coldict: 
        print( 'Invalid row,col array in function numToCoor ' ) 
        return '' 

    else: 
        return coldict[rowcol[1] ]  +  rowdict[ rowcol[0] ] 
    






# # # Testing ---------------------------------------------------
# for j in range(8): 
#     print( '----------------- next row -------------------------------' ) 
#     for k in range(8): 
#         print( numToCoor( [j,k] )  ) 

# for j in range(8): 
#     print( '----------------- next row -------------------------------' ) 
#     for k in range(8): 
#         tempstr = chr(j+ord('a') )  + str(k+1) 
#         print( tempstr , '  -->   ',  coorToNum(tempstr   )   ) 


#  print( numToCoor( [-1,0] ) ) 
#  print( numToCoor( [1,8]  ) ) 
#  print( coorToNum( 'a9' ) ) 
#  print( coorToNum( 'k1' ) ) 
#  








