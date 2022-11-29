#!/bin/python3
# 2022.07.28
# main.py

import pygame

# This is the main program that iniitializes the game.

import genFun as gf
import chessBoard as cb
import chessPiece as cp
import chessMove as cm
import chessPlayer as cp

from chessGame import Game

clock = pygame.time.Clock()

display = pygame.display.set_mode((800, 800))
pygame.display.flip()

# initialFEN = "rnbqkbnr/8/8/8/8/8/8/RNBQKBNR/ w kqKQ - 0 1"
# initialFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR/ w kqKQ - 0 1"

# score = [0, 0]
# color1 = 'w'
# color2 = 'b'

toggleFirstGame = True
game = Game(display)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            game.event(ev)
    
    game.update()
    game.draw()

    pygame.display.update()
    clock.tick(60)

# while True:
#     if toggleFirstGame:
#         toggleFirstGame = False
#     else:
#         color1, color2 = color2, color1

#     # initilize the players
#     player1 = cp.Human(color1)
#     player2 = cp.RandomComp(color2)

#     board = cb.Board(initialFEN)

#     print('player1: ', player1)
#     print('player2: ', player2)

#     cellX = -1
#     cellY = -1
#     while board.checkStatus(board.toMove) == "in prog":
#         for ev in pygame.event.get():
#             if ev.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             elif ev.type == pygame.MOUSEMOTION:
#                 mouseX, mouseY = ev.pos
#                 cellX = mouseX // 100
#                 cellY = mouseY // 100

#         img = board.display()
#         display.blit(img, (0, 0))
#         if cellX >= 0 and cellY >= 0:
#             highlight = pygame.Surface((100, 100)).convert_alpha()
#             highlight.fill((255, 255, 0, 128))
#             display.blit(highlight, (cellX * 100, cellY * 100, 100, 100))
#         pygame.display.update()
#         clock.tick(60)

#         possMoves = board.possibleMoves(board.toMove)

#         # if player1.color == board.toMove:
#         #   move = player1.decideMove( board, possMoves )
#         # else: # player2.color == board.toMove
#         #   move =  player2.decideMove( board, possMoves )

#         # board.executeMove( move )

#         # print( '\n' , move , '\n' )

#     if board.checkStatus(board.toMove) == 'draw':
#         print('\n\n It was a draw! \n\n ')
#         score[0] += 0.5
#         score[1] += 0.5

#     elif board.checkStatus(board.toMove) == 'checkmate':

#         # who ever is to move lost.
#         if board.toMove == player1.color:
#             print('\n\n Player2 was victorious! \n\n')
#             score[1] += 1
#         else:
#             print('\n\n Player1 was victorious! \n\n')
#             score[0] += 1

#     # print( 'Player1: ' ,  score[0] ,  ' vs Player2: ' , score[1] )

#     # while True:
#     #   yesOrNo = input("Play again? (y or n): ").lower()
#     #   if yesOrNo == 'y' or yesOrNo == 'n':
#     #   break

#     # if yesOrNo == 'n':
#     #   break
