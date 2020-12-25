import curses
import math
import time
import random


def main():
    autoQueen0 = [0, 1, 2, 3, 4, 5, 6, 7]
    autoQueen1 = [56, 57, 58, 59, 60, 61, 62, 63]
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.raw()
    curses.noecho()
    curses.cbreak()
    stdscr.nodelay(True)
    stdscr.keypad(True)
    curses.curs_set(0)
    maxyx = stdscr.getmaxyx()
    if (maxyx[0]<60 or maxyx[1]<80):
        screenTooSmall(stdscr)
        curses.endwin()
        exit(1)
    chessPiece = [0, 0, 0]
    chessBoard = genChessBoard()
    moves = genMoves(chessBoard, chessPiece)
    frame = 0
    checkX = 0
    checkX2 = 0
    checkO = 0
    checkO2 = 0
    ifMoves = 0
    seconds = 0
    blink = 0
    offset = 30
    whosTurnIsIt = 0
    chessCurs = 35
    drawTitle(stdscr)
    drawControls(stdscr)
    while(1):
        if (frame>59):
            frame = 0
            seconds += 1
        else:
            frame += 1
        #draw frame
        drawBoard(stdscr, chessBoard, chessPiece, chessCurs, blink, ifMoves, moves)
        drawUI(stdscr, whosTurnIsIt, chessPiece, checkX, checkO)
        #keyboard input
        try:
            c = stdscr.get_wch()
        except:
            c = 0
        #moving, quitting, and all that stuff
        if (c=='q'):
            gameover(stdscr, whosTurnIsIt)
            break
        elif(c=='m'):
            if(ifMoves==0):
                ifMoves = 1
            else:
                ifMoves = 0
        elif(c==' ' and chessBoard[chessCurs][1]==whosTurnIsIt+1):
            chessPiece = [chessBoard[chessCurs][0], chessBoard[chessCurs][1], chessCurs]
        elif(not chessPiece==[0, 0, 0] and (c==chr(10) or c==chr(13)) and chessCurs in moves):
            if(whosTurnIsIt==0):
                whosTurnIsIt = 1
            else:
                whosTurnIsIt = 0
            chessBoard[chessPiece[2]] = [0, 0]
            chessBoard[chessCurs] = [chessPiece[0], chessPiece[1]]
            chessPiece = [0, 0, 0]
            checkX2 = 0
            checkO2 = 0
            for num, i in enumerate(chessBoard):
                if(i[1]==1):
                    tmpMov = genMoves(chessBoard, [i[0], i[1], num])
                    if(chessBoard.index([6, 2]) in tmpMov):
                        checkO2 = 1
                elif(i[1]==2):
                    tmpMov = genMoves(chessBoard, [i[0], i[1], num])
                    if(chessBoard.index([6, 1]) in tmpMov):
                        checkX2 = 1
            if (checkX==1 and checkX2==1):
                checkmate(stdscr, 1)
                break
            if (checkO==1 and checkO2==1):
                checkmate(stdscr, 0)
                break
        elif(c==curses.KEY_UP):
            frame = 50
            if(chessCurs>7):
                chessCurs -= 8
        elif(c==curses.KEY_DOWN):
            frame = 50
            if(chessCurs<56):
                chessCurs += 8
        elif(c==curses.KEY_LEFT):
            frame = 50
            if(chessCurs>0):
                chessCurs -= 1
        elif(c==curses.KEY_RIGHT):
            frame = 50
            if(chessCurs<63):
                chessCurs += 1
        #game loop stuff
        if (frame<offset):
            blink = 1
        else:
            blink = 0
        checkX = 0
        checkO = 0
        for num, i in enumerate(chessBoard):
            if(i[1]==1):
                tmpMov = genMoves(chessBoard, [i[0], i[1], num])
                if(chessBoard.index([6, 2]) in tmpMov):
                    checkO = 1
            elif(i[1]==2):
                tmpMov = genMoves(chessBoard, [i[0], i[1], num])
                if(chessBoard.index([6, 1]) in tmpMov):
                    checkX = 1
        for num, i in enumerate(chessBoard):
            if (i[0]==1 and i[1]==1 and num in autoQueen0):
                i[0] = 5
            elif(i[0]==1 and i[1]==2 and num in autoQueen1):
                i[0] = 5
        if(whosTurnIsIt==0):
            moves = genMoves(chessBoard, chessPiece)
        elif(whosTurnIsIt==1):
            chessBoard, chessPiece, chessCurs, moves = genAIMove(chessBoard, chessPiece, chessCurs, checkO)
            curses.unget_wch(chr(10))
            frame = 50
        for i in moves:
            if(i==chessBoard.index([6, 1])):
                moves.pop(moves.index(i))
            elif(i==chessBoard.index([6, 2])):
                moves.pop(moves.index(i))
        #
        stdscr.refresh()
        time.sleep(0.016)
        stdscr.erase()
    curses.endwin()

def genAIMove(chessBoard, chessPiece, chessCurs, checkO):
    aiPieces = []
    playerMoves = []
    possiblePlayerMoves = []
    pawns = []
    for num, i in enumerate(chessBoard):
        if(i[1]==2 and len(genMoves(chessBoard, [i[0], i[1], num]))>0):
            aiPieces.append([num, genMoves(chessBoard, [i[0], i[1], num])])
    for num, i in enumerate(chessBoard):
        if(i[1]==1 and len(genMoves(chessBoard, [i[0], i[1], num]))>0):
            for j in genMoves(chessBoard, [i[0], i[1], num]):
                playerMoves.append(j)
                possiblePlayerMoves.extend(genMoves(chessBoard, [i[0], i[1], j]))
    for num, i in enumerate(aiPieces):
        if(chessBoard[i[0]]==[1, 2]):
            pawns.append(num)
    dangerTotal = 0
    for i in aiPieces:
        dangerCount = 0
        if(i[0] in playerMoves or i[0] in possiblePlayerMoves):
            dangerCount -= 1
        for j in i[1]:
            if(j in playerMoves or j in possiblePlayerMoves):
                dangerCount -= 1
        dangerTotal -= dangerCount
        i.append(dangerCount)
    totalMovCount = 0
    for i in aiPieces:
        goodMovCount = 0
        for num, j in enumerate(i[1]):
            if(chessBoard[j][0]==5):
                goodMovCount += 9
            elif(chessBoard[j][0]==4):
                goodMovCount += 3
            elif(chessBoard[j][0]==3):
                goodMovCount += 3
            elif(chessBoard[j][0]==2):
                goodMovCount += 5
            elif(chessBoard[j][0]==1):
                goodMovCount += 1
        totalMovCount += goodMovCount
        i.append(goodMovCount)
    for i in aiPieces:
        i[2] = (i[2]+i[3])/2
        i.pop(3)
    aiPieces.sort(reverse=True, key=lambda sorter: sorter[2])
    for i in aiPieces:
        i.pop(2)
    if(totalMovCount<1 and dangerTotal>-1 and checkO==0 and len(pawns)>0):
        aiPieces.insert(0, aiPieces.pop(random.choice(pawns)))
    for i in aiPieces:
        for num, j in enumerate(i[1]):
            if(chessBoard[j][0]==6):
                i[1] = []
                break
            elif(chessBoard[j][0]==5):
                i[1].insert(0, i[1].pop(num))
            elif(chessBoard[j][0]==4):
                i[1].insert(0, i[1].pop(num))
            elif(chessBoard[j][0]==3):
                i[1].insert(0, i[1].pop(num))
            elif(chessBoard[j][0]==2):
                i[1].insert(0, i[1].pop(num))
            elif(chessBoard[j][0]==1):
                i[1].insert(0, i[1].pop(num))
    k = chessBoard.index([6, 2])
    for num, i in enumerate(aiPieces):
        if(i[0]==k):
            k = num
            break
    for i in aiPieces[k][1]:
        if(i in playerMoves or i in possiblePlayerMoves):
            aiPieces[k][1].pop(aiPieces[k][1].index(i))
    if(checkO==1):
        for num, i in enumerate(aiPieces):
            if(chessBoard[i[0]]==[6,2]):
                aiPieces.insert(0, aiPieces.pop(num))
        for i in aiPieces[0][1]:
            if(i in playerMoves):
                aiPieces[0][1].pop(aiPieces[0][1].index(i))
        if(len(aiPieces[0][1])==0):
            aiPieces.insert(0, aiPieces.pop(1))
    aiPiece = aiPieces[0][0]
    chessCurs = aiPieces[0][1][0]
    chessPiece = [chessBoard[aiPiece][0], chessBoard[aiPiece][1], aiPiece]
    moves = genMoves(chessBoard, chessPiece)
    return chessBoard, chessPiece, chessCurs, moves

def checkmate(stdscr, winner):
    maxyx = stdscr.getmaxyx()
    stdscr.erase()
    if (winner==0):
        line0 = "Red won by Checkmate!"
    else:
        line0 = "Blue won by Checkmate!"
    stdscr.addstr(int(maxyx[0]/2), int(maxyx[1]/2-len(line0)/2), line0)
    stdscr.refresh()
    time.sleep(4)

def genMoves(chessBoard, chessPiece): 
    moves = []
    walls0 = [0, 8, 16, 24, 32, 40, 48, 56]
    walls1 = [7, 15, 23, 31, 39, 47, 55, 63]
    walls02 = []
    walls12 = []
    for i in walls0:
        walls02.append(i+1)
    for i in walls1:
        walls12.append(i-1)
    #knightArr = [15, 17, 6, 10]
    knightArr = [-15, -6, 10, 17, 15, 6, -10, -17]
    kingArr = [1, 7, 8, 9]
    pawnArr0 = []
    pawnArr1 = []
    for i in range(8, 16):
        pawnArr0.append([i, i+16])
    for i in range(48, 56):
        pawnArr1.append([i, i-16])
    if (chessPiece[1]==1):
        if(chessPiece[0]==1):
            if(chessBoard[chessPiece[2]-8]==[0, 0]):
                moves.append(chessPiece[2]-8)
            if(chessBoard[chessPiece[2]-7][1]==2 and chessPiece[2] not in walls1):
                moves.append(chessPiece[2]-7)
            if(chessBoard[chessPiece[2]-9][1]==2 and chessPiece[2] not in walls0):
                moves.append(chessPiece[2]-9)
            for i in pawnArr1:
                if(chessPiece[2]==i[0] and chessBoard[i[1]]==[0, 0]):
                    moves.append(i[1])
        elif(chessPiece[0]==2):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif (i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif (i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==3):
            for num, i in enumerate(knightArr):
                if(chessPiece[2] in walls1 and i in [-15, -6, 10, 17]):
                    continue
                if(chessPiece[2] in walls0 and i in [15, 6, -10, -17]):
                    continue
                elif(chessPiece[2] in walls12 and i in [-6, 10]):
                    continue
                elif(chessPiece[2] in walls02 and i in [6, -10]):
                    continue
                if(i%-1==0):
                    if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=1):
                        moves.append(chessPiece[2]+i)
                else:
                    if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=1):
                        moves.append(chessPiece[2]-i)
        elif(chessPiece[0]==4):
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==5):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==1):
                    break
                elif(chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif (i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif (i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==1 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==2):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==6):
            for i in kingArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=1):
                    if(not ((i==7 or i==1) and chessPiece[2] in walls0)):
                        moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=1):
                    if(not ((i==9 or i==1) and chessPiece[2] in walls1)):
                        moves.append(chessPiece[2]+i)
    elif (chessPiece[1]==2):
        if(chessPiece[0]==1):
            if(chessBoard[chessPiece[2]+8]==[0, 0]):
                moves.append(chessPiece[2]+8)
            if(chessBoard[chessPiece[2]+7][1]==1 and chessPiece[2] not in walls0):
                moves.append(chessPiece[2]+7)
            if(chessBoard[chessPiece[2]+9][1]==1 and chessPiece[2] not in walls1):
                moves.append(chessPiece[2]+9)
            for i in pawnArr0:
                if(chessPiece[2]==i[0] and chessBoard[i[1]]==[0, 0]):
                    moves.append(i[1])
        elif(chessPiece[0]==2):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif (i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif (i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==3):
            for num, i in enumerate(knightArr):
                if(chessPiece[2] in walls1 and i in [-15, -6, 10, 17]):
                    continue
                if(chessPiece[2] in walls0 and i in [15, 6, -10, -17]):
                    continue
                elif(chessPiece[2] in walls12 and i in [-6, 10]):
                    continue
                elif(chessPiece[2] in walls02 and i in [6, -10]):
                    continue
                if(i%-1==0):
                    if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=2):
                        moves.append(chessPiece[2]+i)
                else:
                    if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=2):
                        moves.append(chessPiece[2]-i)
        elif(chessPiece[0]==4):
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==5):
            for i in range(chessPiece[2]-8, -1, -8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+8, 64, 8):
                if (chessBoard[i][1]==2):
                    break
                elif(chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+1, chessPiece[2]+int(8)):
                if (i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif (i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-1, chessPiece[2]-int(8), -1):
                if (i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif (i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-7, -1, -7):
                if(i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]-9, -1, -9):
                if(i<0 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+7, 64, 7):
                if(i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls0):
                    break
                elif(i in walls0 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
            for i in range(chessPiece[2]+9, 64, 9):
                if(i>63 or chessBoard[i][1]==2 or chessPiece[2] in walls1):
                    break
                elif(i in walls1 or chessBoard[i][1]==1):
                    moves.append(i)
                    break
                else:
                    moves.append(i)
        elif(chessPiece[0]==6):
            for i in kingArr:
                if(chessPiece[2]-i>=0 and chessPiece[2]-i<=63 and chessBoard[chessPiece[2]-i][1]!=2):
                    if(not ((i==7 or i==1) and chessPiece[2] in walls0)):
                        moves.append(chessPiece[2]-i)
                if(chessPiece[2]+i>=0 and chessPiece[2]+i<=63 and chessBoard[chessPiece[2]+i][1]!=2):
                    if(not ((i==9 or i==1) and chessPiece[2] in walls1)):
                        moves.append(chessPiece[2]+i)
    return moves

def drawUI(stdscr, turn, piece, x, o):
    if(turn==0):
        stdscr.addstr(1, 1, "X's turn to play")
    else:
        stdscr.addstr(1, 1, "O's turn to play")
    if(piece[0]==1):
        line0 = "Pawn"
    elif(piece[0]==2):
        line0 = "Rook"
    elif(piece[0]==3):
        line0 = "Knight"
    elif(piece[0]==4):
        line0 = "Bishop"
    elif(piece[0]==5):
        line0 = "Queen"
    elif(piece[0]==6):
        line0 = "King"
    else:
        line0 = "None"
    stdscr.addstr(3, 1, str("Selected Piece: "+line0))
    if(x==1 and o==1):
        line1 = "X and O are in Check!!"
    elif(x==1 and o==0):
        line1 = "X is in Check!!"
    elif(x==0 and o==1):
        line1 = "O is in Check!!"
    else:
        line1 = ''
    stdscr.addstr(5, 1, line1)

def drawBoard(stdscr, chessBoard, chessPiece, chessCurs, ifBlinkOn, ifMoves, moves):
    maxyx = stdscr.getmaxyx()
    topLeftCorner = [math.trunc(maxyx[0]/2-25), math.trunc(maxyx[1]/2-40)]
    curs = [topLeftCorner[0], topLeftCorner[1]]
    checkerboard = ('.', ';', '.', ';', '.', ';', '.', ';', 
            ';', '.', ';', '.', ';', '.', ';', '.', 
            '.', ';', '.', ';', '.', ';', '.', ';', 
            ';', '.', ';', '.', ';', '.', ';', '.', 
            '.', ';', '.', ';', '.', ';', '.', ';', 
            ';', '.', ';', '.', ';', '.', ';', '.', 
            '.', ';', '.', ';', '.', ';', '.', ';', 
            ';', '.', ';', '.', ';', '.', ';', '.', )
    pieces0 = [["   /\\    ","   \\/    ","   XX    ","   XX    ","  XXXX   "],
            ["  X  X   ","  XXXX   ","   XX    ","   XX    ","  XXXX   "],
            ["   XX    ","  XXXX   ","  XX     ","   XX    ","  XXXX   "],
            ["   /.    ","   \\/    ","   /\\    ","   XX    ","  XXXX   "],
            ["  ____   ","  ||||   ","   XX    ","   XX    ","  XXXX   "],
            ["   ||    ","  =XX=   ","   ||    ","   XX    ","  XXXX   "]]
    pieces1 = [["   /\\    ","   \\/    ","   OO    ","   OO    ","  OOOO   "],
            ["  O  O   ","  OOOO   ","   OO    ","   OO    ","  OOOO   "],
            ["   OO    ","  OOOO   ","  OO     ","   OO    ","  OOOO   "],
            ["   /.    ","   \\/    ","   /\\    ","   OO    ","  OOOO   "],
            ["  ____   ","  ||||   ","   OO    ","   OO    ","  OOOO   "],
            ["   ||    ","  =OO=   ","   ||    ","   OO    ","  OOOO   "]]
    #line0 = "+---------+---------+---------+---------+---------+---------+---------+---------+"
    line0 = [curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_PLUS]
    #line1 = "|         |         |         |         |         |         |         |         |"
    line1 = [curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', curses.ACS_VLINE]
    for x in range(8):
        if(x==0):
            stdscr.addch(curs[0]+3, curs[1]-2, '8')
        if(x==1):
            stdscr.addch(curs[0]+3, curs[1]-2, '7')
        if(x==2):
            stdscr.addch(curs[0]+3, curs[1]-2, '6')
        if(x==3):
            stdscr.addch(curs[0]+3, curs[1]-2, '5')
        if(x==4):
            stdscr.addch(curs[0]+3, curs[1]-2, '4')
        if(x==5):
            stdscr.addch(curs[0]+3, curs[1]-2, '3')
        if(x==6):
            stdscr.addch(curs[0]+3, curs[1]-2, '2')
        if(x==7):
            stdscr.addch(curs[0]+3, curs[1]-2, '1')
        for i in line0:
            stdscr.addch(curs[0], curs[1], i)
            curs[1] += 1
        curs[0] += 1
        curs[1] = topLeftCorner[1]
        for y in range(5):
            for j in line1:
                stdscr.addch(curs[0], curs[1], j)
                curs[1] += 1
            curs[0] += 1
            curs[1] = topLeftCorner[1]
    for num, i in enumerate(line0):
        if (num==0):
            stdscr.addch(curs[0]+1, curs[1]+5, 'a')
        if (num==10):
            stdscr.addch(curs[0]+1, curs[1]+5, 'b')
        if (num==20):
            stdscr.addch(curs[0]+1, curs[1]+5, 'c')
        if (num==30):
            stdscr.addch(curs[0]+1, curs[1]+5, 'd')
        if (num==40):
            stdscr.addch(curs[0]+1, curs[1]+5, 'e')
        if (num==50):
            stdscr.addch(curs[0]+1, curs[1]+5, 'f')
        if (num==60):
            stdscr.addch(curs[0]+1, curs[1]+5, 'g')
        if (num==70):
            stdscr.addch(curs[0]+1, curs[1]+5, 'h')
        stdscr.addch(curs[0], curs[1], i)
        curs[1] += 1
    curs = [topLeftCorner[0], topLeftCorner[1]]
    for num, i in enumerate(chessBoard):
        curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        for j in range(5):
            for x in range(9):
                if(checkerboard[num]=='.'):
                    stdscr.addch(curs[0], curs[1]+x, checkerboard[num], curses.color_pair(3))
                else:
                    stdscr.addch(curs[0], curs[1]+x, checkerboard[num], curses.color_pair(4))
            curs[0] += 1
        curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        if (num in moves and ifMoves==1):
            for j in range(5):
                for x in range(9):
                    stdscr.addch(curs[0], curs[1]+x, '@', curses.color_pair(chessPiece[1]))
                curs[0] += 1
        curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        if (num==chessCurs and ifBlinkOn!=1):
            for j in range(5):
                for x in range(9):
                    stdscr.addch(curs[0], curs[1]+x, '#', curses.color_pair(5))
                curs[0] += 1
            curs = [math.trunc(topLeftCorner[0]+int(num/8)*6)+1, math.trunc(topLeftCorner[1]+(num%8)*10)+1]
        if (i[1]==0):
            pass
        elif (i[1]==1):
            for j in pieces0[i[0]-1]:
                for x, c in enumerate(j):
                    if (c==' '):
                        pass
                    else:
                        stdscr.addch(curs[0], curs[1]+x, c, curses.color_pair(1))
                curs[0] += 1
        else:
            for j in pieces1[i[0]-1]:
                for x, c in enumerate(j):
                    if (c==' '):
                        pass
                    else:
                        stdscr.addch(curs[0], curs[1]+x, c, curses.color_pair(2))
                curs[0] += 1

def screenTooSmall(stdscr):
    maxyx = stdscr.getmaxyx()
    stdscr.erase()
    line0 = "Your terminal window isn't big enough"
    stdscr.addstr(math.trunc(maxyx[0]/2), math.trunc(maxyx[1]/2-(len(line0)/2)), line0)
    stdscr.refresh()
    while(stdscr.getch()==curses.ERR):
        time.sleep(0.016)

def genChessBoard():
    lst = []
    #[[x, y] * 64]     :       x = type of piece   y = team of piece
    #                           0-7                 0-2
    for i in range(64):
        lst.append([0, 0])
    #pawns
    for i in range(8, 16):
        lst[i] = [1, 2]
    for i in range(48, 56):
        lst[i] = [1, 1]
    #rooks
    lst[0] = [2, 2]
    lst[7] = [2, 2]
    lst[56] = [2, 1]
    lst[63] = [2, 1]
    #knights
    lst[1] = [3, 2]
    lst[6] = [3, 2]
    lst[57] = [3, 1]
    lst[62] = [3, 1]
    #bishops
    lst[2] = [4, 2]
    lst[5] = [4, 2]
    lst[58] = [4, 1]
    lst[61] = [4, 1]
    #queens
    lst[3] = [5, 2]
    lst[59] = [5, 1]
    #kings
    lst[4] = [6, 2]
    lst[60] = [6, 1]
    return lst

def drawControls(stdscr):
    maxyx = stdscr.getmaxyx()
    stdscr.clear()
    controlsbox = curses.newwin(math.trunc(maxyx[0]*3/5), math.trunc(maxyx[1]/3), math.trunc(maxyx[0]/5), math.trunc(maxyx[1]/3))
    curses.raw()
    curses.noecho()
    curses.cbreak()
    controlsbox.nodelay(True)
    controlsbox.keypad(True)
    maxyx1 = controlsbox.getmaxyx()
    controlsbox.border()
    line0 = "Controls:"
    line1 = "q - Quit"
    line2 = "Arrow Keys - Move Cursor"
    line3 = "m - Show Moves"
    line4 = "Space - Select Piece"
    line5 = "Enter - Move Piece"
    controlsbox.move(math.trunc(maxyx1[0]/2)-5, math.trunc(maxyx1[1]/2-len(line0)/2))
    controlsbox.addstr(line0)
    controlsbox.move(math.trunc(maxyx1[0]/2)-1, math.trunc(maxyx1[1]/2-len(line1)/2))
    controlsbox.addstr(line1)
    controlsbox.move(math.trunc(maxyx1[0]/2)+1, math.trunc(maxyx1[1]/2-len(line2)/2))
    controlsbox.addstr(line2)
    controlsbox.move(math.trunc(maxyx1[0]/2)+3, math.trunc(maxyx1[1]/2-len(line3)/2))
    controlsbox.addstr(line3)
    controlsbox.move(math.trunc(maxyx1[0]/2)+5, math.trunc(maxyx1[1]/2-len(line4)/2))
    controlsbox.addstr(line4)
    controlsbox.move(math.trunc(maxyx1[0]/2)+7, math.trunc(maxyx1[1]/2-len(line5)/2))
    controlsbox.addstr(line5)
    stdscr.refresh()
    controlsbox.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 600):
        frame += 1
        time.sleep(0.016)
    controlsbox.clear()
    stdscr.clear()
    controlsbox.refresh()
    stdscr.refresh()


def drawTitle(stdscr):
    maxyx = stdscr.getmaxyx()
    title = ["        CCCCCCCCCCCCChhhhhhh                                                                         ", "        CCC::::::::::::Ch:::::h                                                                            ", "   CC:::::::::::::::Ch:::::h                                                                        ", "   C:::::CCCCCCCC::::Ch:::::h                                                                          ", "                           C:::::C       CCCCCC h::::h hhhhh           eeeeeeeeeeee        ssssssssss       ssssssssss                                     ", "  C:::::C               h::::hh:::::hhh      ee::::::::::::ee    ss::::::::::s    ss::::::::::s            ", "   C:::::C               h::::::::::::::hh   e::::::eeeee:::::eess:::::::::::::s ss:::::::::::::s            ", " C:::::C               h:::::::hhh::::::h e::::::e     e:::::es::::::ssss:::::ss::::::ssss:::::s        ", "C:::::C               h::::::h   h::::::he:::::::eeeee::::::e s:::::s  ssssss  s:::::s  ssssss        ", "C:::::C               h:::::h     h:::::he:::::::::::::::::e    s::::::s         s::::::s             ", "C:::::C               h:::::h     h:::::he::::::eeeeeeeeeee        s::::::s         s::::::s          ", "   C:::::C       CCCCCC h:::::h     h:::::he:::::::e           ssssss   s:::::s ssssss   s:::::s          ", "C:::::CCCCCCCC::::C h:::::h     h:::::he::::::::e          s:::::ssss::::::ss:::::ssss::::::s     ", "    CC:::::::::::::::C h:::::h     h:::::h e::::::::eeeeeeee  s::::::::::::::s s::::::::::::::s         ", "CCC::::::::::::C h:::::h     h:::::h  ee:::::::::::::e   s:::::::::::ss   s:::::::::::ss    ", "            CCCCCCCCCCCCC hhhhhhh     hhhhhhh    eeeeeeeeeeeeee    sssssssssss      sssssssssss               "]
    for num, i in enumerate(range(int(0-len(title)/2), int(len(title)/2))):
        stdscr.move(math.trunc(maxyx[0]/2+i), math.trunc(maxyx[1]/2-math.trunc(len(title[num])/2)))
        for j in title[num]:
            if(j==' '):
                color = 3
            elif(i%2==0):
                color = 6
            else:
                color = 7
            try:
                stdscr.addch(j, curses.color_pair(color))
            except:
                pass
    stdscr.refresh()
    time.sleep(1)
    curses.flushinp()
    frame = 0
    while(stdscr.getch()==curses.ERR and frame < 60):
        frame += 1
        time.sleep(0.016)

def gameover(stdscr, turn):
    maxyx = stdscr.getmaxyx()
    if(turn==0):
        line0 = "Quit during X's turn"
    else:
        line0 = "Quit during O's turn"
    stdscr.clear()
    stdscr.move(math.trunc(maxyx[0]/2-1), math.trunc(maxyx[1]/2-math.trunc(len(line0)/2)))
    stdscr.addstr(line0)
    stdscr.refresh()
    time.sleep(2)
    curses.flushinp()
    frame = 0
    while (stdscr.getch()==curses.ERR and frame < 600):
        time.sleep(0.016)
        frame += 1

if __name__ == '__main__':
    main()
